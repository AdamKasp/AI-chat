from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.repository.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)

class DeleteUserController:
    @staticmethod
    async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db_session)
    ) -> dict:
        try:
            repository = UserRepository(db)
            
            user = await repository.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            success = await repository.delete_user(user_id)
            
            if success:
                return {"message": "User deleted successfully"}
            else:
                raise HTTPException(status_code=500, detail="Failed to delete user")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_user endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))