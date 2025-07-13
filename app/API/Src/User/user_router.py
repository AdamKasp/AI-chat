from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.User.controller.create_user import CreateUserController
from app.API.Src.User.request.user_request import UserCreateRequest
from app.API.Src.User.controller.get_user_list import GetUserListController
from app.API.Src.User.controller.get_user import GetUserController
from app.API.Src.User.controller.delete_user import DeleteUserController
from app.API.Src.User.response.user_response import UserResponse
from app.API.Src.User.response.user_list_response import UserListResponse

router = APIRouter()

@router.post("/users", response_model=UserResponse, tags=["Users"])
async def create_user(user_request: UserCreateRequest, db: AsyncSession = Depends(get_db_session)):
    return await CreateUserController.create_user(user_request, db)

@router.get("/users", response_model=UserListResponse, tags=["Users"])
async def get_users(limit: int = Query(default=100, le=1000), offset: int = Query(default=0, ge=0), db: AsyncSession = Depends(get_db_session)):
    return await GetUserListController.get_users(limit, offset, db)

@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await GetUserController.get_user(user_id, db)

@router.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await DeleteUserController.delete_user(user_id, db)