from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.repository.document_repository import DocumentRepository
import logging

logger = logging.getLogger(__name__)

class DeleteDocumentController:
    @staticmethod
    async def delete_document(
        document_id: UUID,
        db: AsyncSession = Depends(get_db_session)
    ) -> dict:
        try:
            repository = DocumentRepository(db)
            success = await repository.delete_document(document_id)
            
            if not success:
                raise HTTPException(status_code=404, detail="Document not found")
            
            return {"message": f"Document {document_id} deleted successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_document endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))