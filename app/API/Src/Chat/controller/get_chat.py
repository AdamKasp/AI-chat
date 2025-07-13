from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.response.chat_response import ChatResponse, MessageResponse
import logging

logger = logging.getLogger(__name__)

class GetChatController:
    @staticmethod
    async def get_chat(
        chat_id: UUID,
        db: AsyncSession = Depends(get_db_session)
    ) -> ChatResponse:
        try:
            repository = ChatRepository(db)
            chat = await repository.get_chat_with_messages(chat_id)
            
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            
            messages = []
            if chat.messages:
                messages = [
                    MessageResponse(
                        id=str(msg.id),
                        message=msg.message,
                        author=msg.author,
                        created_at=msg.created_at
                    )
                    for msg in chat.messages
                ]
            
            return ChatResponse(
                id=str(chat.id),
                user_id=str(chat.user_id),
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                messages=messages
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_chat endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))