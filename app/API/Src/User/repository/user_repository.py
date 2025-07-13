from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.API.Src.User.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, login: str) -> User:
        user = User(login=login)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_login(self, login: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.login == login)
        )
        return result.scalar_one_or_none()
    
    async def get_users_paginated(self, limit: int = 100, offset: int = 0) -> Tuple[List[User], int]:
        count_result = await self.session.execute(
            select(func.count(User.id))
        )
        total = count_result.scalar()
        
        result = await self.session.execute(
            select(User)
            .order_by(User.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all(), total
    
    async def delete_user(self, user_id: UUID) -> bool:
        result = await self.session.execute(
            delete(User).where(User.id == user_id)
        )
        await self.session.commit()
        return result.rowcount > 0