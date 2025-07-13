from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from typing import Optional, List
from uuid import UUID
from pathlib import Path
import aiofiles
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.repository.document_repository import DocumentRepository
from app.API.Src.Document.response.document_response import DocumentResponse
from app.API.Src.Document.response.document_list_response import DocumentListResponse
from app.API.Src.Document.response.document_upload_response import DocumentUploadResponse
from app.API.Src.core.ExternalApiHelper.OpenAI.embedding_generator import EmbeddingGenerator
from app.API.Src.core.database.Qdrant.repository import QdrantRepository
from app.API.Src.core.database.Qdrant.models import VectorSearchQuery
from app.API.Src.core.config import settings
from app.API.Src.Document.documentSplitter.token_based_text_splitter import TextSplitter
from app.API.Src.Document.models.document import Document
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/documents", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        # Validate file format
        if not file.filename.endswith('.md'):
            raise HTTPException(status_code=400, detail="Only .md files are allowed")
        
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Create Corpus directory if not exists
        corpus_path = Path(settings.corpus_absolute_path)
        corpus_path.mkdir(exist_ok=True)
        
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_parts = file.filename.rsplit('.', 1)
        new_filename = f"{name_parts[0]}_{current_date}.{name_parts[1]}"
        file_path = corpus_path / new_filename
        
        # Save file to Corpus directory
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Split document using TokenBasedTextSplitter
        text_splitter = TextSplitter()
        token_limit = settings.DOCUMENT_TOKEN_LIMIT
        split_documents = await text_splitter.split(content_str, limit=token_limit)
        
        logger.info(f"Split document into {len(split_documents)} parts")
        
        repository = DocumentRepository(db)
        saved_documents: List[Document] = []
        
        # Process each split document
        for i, split_doc in enumerate(split_documents):
            # Set the localisation for each split document
            split_doc.localisation = f"{file_path.stem}_part_{i+1:03d}.md"
            
            # Save to both PostgreSQL and Qdrant
            saved_doc = await repository.save_document(split_doc, str(file_path))
            saved_documents.append(saved_doc)
            
            logger.info(f"Saved document part {i+1}/{len(split_documents)}: {saved_doc.id}")
        
        # Return response for the first document (or summary)
        first_doc = saved_documents[0] if saved_documents else None
        if not first_doc:
            raise HTTPException(status_code=500, detail="Failed to process document")
        
        return DocumentUploadResponse(
            id=str(first_doc.id),
            localisation=first_doc.localisation,
            message=f"Document uploaded and split into {len(saved_documents)} parts successfully",
            created_at=first_doc.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents", response_model=DocumentListResponse, tags=["Documents"])
async def get_documents(
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = DocumentRepository(db)
        documents, total = await repository.get_documents_paginated(limit=limit, offset=offset)
        
        document_responses = [
            DocumentResponse.from_document(doc)
            for doc in documents
        ]
        
        return DocumentListResponse(
            documents=document_responses,
            total=total,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error in get_documents endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/search", response_model=list, tags=["Documents"])
async def search_documents(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=10, le=50),
    score_threshold: Optional[float] = Query(default=None, description="Minimum similarity score")
):
    try:
        embedding_generator = EmbeddingGenerator()
        qdrant_repo = QdrantRepository()
        
        # Generate embedding for query
        query_embedding = await embedding_generator.generate_embedding(query)
        
        # Create search query
        search_query = VectorSearchQuery(
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold
        )
        
        results = await qdrant_repo.search_similar(search_query)
        
        return [
            {
                "id": result.id,
                "content": result.content,  # Now contains summary
                "file_path": result.file_path,  # Will be empty
                "score": result.score,
                "metadata": result.metadata
            }
            for result in results
        ]
        
    except Exception as e:
        logger.error(f"Error in search_documents endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}", response_model=DocumentResponse, tags=["Documents"])
async def get_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = DocumentRepository(db)
        document = await repository.get_document_by_id(document_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Debug log
        logger.info(f"Document from DB - tokens: {document.tokens}, type: {type(document.tokens)}")
        logger.info(f"Document attributes: {[attr for attr in dir(document) if not attr.startswith('_')]}")
        
        return DocumentResponse.from_document(document)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_document endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))