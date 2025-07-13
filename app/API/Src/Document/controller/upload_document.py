from fastapi import HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import aiofiles
from datetime import datetime
from typing import List
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.repository.document_repository import DocumentRepository
from app.API.Src.Document.response.document_upload_response import DocumentUploadResponse
from app.API.Src.core.config import settings
from app.API.Src.Document.documentSplitter.token_based_text_splitter import TextSplitter
from app.API.Src.Document.models.document import Document
import logging

logger = logging.getLogger(__name__)

class UploadDocumentController:
    @staticmethod
    async def upload_document(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db_session)
    ) -> DocumentUploadResponse:
        try:
            if not file.filename.endswith('.md'):
                raise HTTPException(status_code=400, detail="Only .md files are allowed")
            
            content = await file.read()
            content_str = content.decode('utf-8')
            
            corpus_path = Path(settings.corpus_absolute_path)
            corpus_path.mkdir(exist_ok=True)
            
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = file.filename.rsplit('.', 1)
            new_filename = f"{name_parts[0]}_{current_date}.{name_parts[1]}"
            file_path = corpus_path / new_filename
            
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