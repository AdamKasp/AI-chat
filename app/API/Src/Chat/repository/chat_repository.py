from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.API.Src.Chat.models.chat_history import ChatHistory
import logging

logger = logging.getLogger(__name__)

class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_chat(self, user_id: UUID) -> ChatHistory:
        """Create a new chat conversation"""
        try:
            chat_history = ChatHistory(user_id=user_id)
            self.session.add(chat_history)
            await self.session.commit()
            await self.session.refresh(chat_history)
            logger.info(f"Created new chat {chat_history.id} for user {user_id}")
            return chat_history
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating chat: {str(e)}")
            raise

    async def get_chat_with_messages(self, chat_id: UUID) -> Optional[ChatHistory]:
        """Get chat with all its messages loaded"""
        try:
            result = await self.session.execute(
                select(ChatHistory)
                .options(selectinload(ChatHistory.messages))
                .where(ChatHistory.id == chat_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching chat {chat_id}: {str(e)}")
            return None
    
    async def get_conversation_by_id(self, conversation_id: UUID) -> Optional[ChatHistory]:
        result = await self.session.execute(
            select(ChatHistory).where(ChatHistory.id == conversation_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_conversations(self, limit: int = 100) -> List[ChatHistory]:
        result = await self.session.execute(
            select(ChatHistory)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_conversations_paginated(self, limit: int = 100, offset: int = 0) -> Tuple[List[ChatHistory], int]:
        # Get total count
        count_result = await self.session.execute(
            select(func.count(ChatHistory.id))
        )
        total = count_result.scalar()
        
        # Get paginated results
        result = await self.session.execute(
            select(ChatHistory)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all(), total
    
    async def get_conversations_by_user_paginated(self, user_id: UUID, limit: int = 100, offset: int = 0) -> Tuple[List[ChatHistory], int]:
        # Get total count for user
        count_result = await self.session.execute(
            select(func.count(ChatHistory.id)).where(ChatHistory.user_id == user_id)
        )
        total = count_result.scalar()
        
        # Get paginated results for user
        result = await self.session.execute(
            select(ChatHistory)
            .where(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all(), total