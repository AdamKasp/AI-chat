from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.repository.user_repository import UserRepository
from app.API.Src.User.response.user_response import UserResponse
import logging

logger = logging.getLogger(__name__)

class GetUserController:
    @staticmethod
    async def get_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db_session)
    ) -> UserResponse:
        try:
            repository = UserRepository(db)
            user = await repository.get_user_by_id(user_id)
            
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return UserResponse(
                id=str(user.id),
                login=user.login,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_user endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))