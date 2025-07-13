from fastapi import HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.repository.document_repository import DocumentRepository
from app.API.Src.Document.response.document_response import DocumentResponse
from app.API.Src.Document.response.document_list_response import DocumentListResponse
import logging

logger = logging.getLogger(__name__)

class GetDocumentListController:
    @staticmethod
    async def get_documents(
        limit: int = Query(default=100, le=1000),
        offset: int = Query(default=0, ge=0),
        db: AsyncSession = Depends(get_db_session)
    ) -> DocumentListResponse:
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