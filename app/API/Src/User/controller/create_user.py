from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.repository.user_repository import UserRepository
from app.API.Src.User.response.user_response import UserResponse
from app.API.Src.User.request.user_request import UserCreateRequest
import logging

logger = logging.getLogger(__name__)

class CreateUserController:
    @staticmethod
    async def create_user(
        user_request: UserCreateRequest,
        db: AsyncSession = Depends(get_db_session)
    ) -> UserResponse:
        try:
            repository = UserRepository(db)
            
            existing_user = await repository.get_user_by_login(user_request.login)
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this login already exists")
            
            user = await repository.create_user(login=user_request.login)
            
            return UserResponse(
                id=str(user.id),
                login=user.login,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))