from fastapi import HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.repository.user_repository import UserRepository
from app.API.Src.User.response.user_response import UserResponse
from app.API.Src.User.response.user_list_response import UserListResponse
import logging

logger = logging.getLogger(__name__)

class GetUserListController:
    @staticmethod
    async def get_users(
        limit: int = Query(default=100, le=1000),
        offset: int = Query(default=0, ge=0),
        db: AsyncSession = Depends(get_db_session)
    ) -> UserListResponse:
        try:
            repository = UserRepository(db)
            users, total = await repository.get_users_paginated(limit=limit, offset=offset)
            
            user_responses = [
                UserResponse(
                    id=str(user.id),
                    login=user.login,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in users
            ]
            
            return UserListResponse(
                users=user_responses,
                total=total,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error in get_users endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))