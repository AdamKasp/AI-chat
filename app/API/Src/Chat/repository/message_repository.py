from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from uuid import UUID
from typing import List, Optional
from app.API.Src.Chat.models.message import Message
from app.API.Src.Chat.models.chat_history import ChatHistory
import logging

logger = logging.getLogger(__name__)

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_conversation_messages(self, chat_id: UUID) -> List[Message]:
        """Get all messages for a specific conversation ordered by creation time"""
        try:
            result = await self.db.execute(
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching conversation messages for chat_id {chat_id}: {str(e)}")
            return []

    async def save_message(self, chat_id: UUID, user_id: UUID, message: str, author: str) -> Message:
        """Save a new message to the conversation"""
        try:
            new_message = Message(
                chat_id=chat_id,
                user_id=user_id,
                message=message,
                author=author
            )
            
            self.db.add(new_message)
            await self.db.commit()
            await self.db.refresh(new_message)
            
            logger.info(f"Saved message from {author} in chat {chat_id}")
            return new_message
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error saving message: {str(e)}")
            raise

    async def get_recent_messages(self, chat_id: UUID, limit: int = 10) -> List[Message]:
        """Get the most recent messages for context (limited for performance)"""
        try:
            result = await self.db.execute(
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            # Return in chronological order (oldest first)
            return list(reversed(messages))
        except Exception as e:
            logger.error(f"Error fetching recent messages for chat_id {chat_id}: {str(e)}")
            return []
    
    async def delete_by_chat_id(self, chat_id: UUID) -> None:
        """Delete all messages associated with a chat"""
        try:
            await self.db.execute(
                delete(Message).where(Message.chat_id == chat_id)
            )
            await self.db.commit()
            logger.info(f"Deleted all messages for chat {chat_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting messages for chat {chat_id}: {str(e)}")
            raise