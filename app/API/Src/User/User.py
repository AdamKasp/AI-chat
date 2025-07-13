from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.repository.user_repository import UserRepository
from app.API.Src.User.response.user_response import UserResponse
from app.API.Src.User.response.user_list_response import UserListResponse
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class UserCreateRequest(BaseModel):
    login: str

@router.post("/users", response_model=UserResponse, tags=["Users"])
async def create_user(
    user_request: UserCreateRequest,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = UserRepository(db)
        
        # Check if user already exists
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

@router.get("/users", response_model=UserListResponse, tags=["Users"])
async def get_users(
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db_session)
):
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

@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
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

@router.delete("/users/{user_id}", tags=["Users"])
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = UserRepository(db)
        
        # Check if user exists
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