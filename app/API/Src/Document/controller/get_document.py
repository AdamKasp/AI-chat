from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.repository.document_repository import DocumentRepository
from app.API.Src.Document.response.document_response import DocumentResponse
import logging

logger = logging.getLogger(__name__)

class GetDocumentController:
    @staticmethod
    async def get_document(
        document_id: UUID,
        db: AsyncSession = Depends(get_db_session)
    ) -> DocumentResponse:
        try:
            repository = DocumentRepository(db)
            document = await repository.get_document_by_id(document_id)
            
            if not document:
                raise HTTPException(status_code=404, detail="Document not found")
            
            return DocumentResponse.from_document(document)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_document endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))