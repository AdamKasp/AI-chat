from fastapi import HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.response.chat_response import ChatResponse, MessageResponse
from app.API.Src.Chat.response.chat_list_response import ChatListResponse
import logging

logger = logging.getLogger(__name__)

class GetChatListController:
    @staticmethod
    async def get_chats(
        limit: int = Query(default=100, le=1000),
        offset: int = Query(default=0, ge=0),
        user_id: Optional[UUID] = Query(default=None, description="Filter chats by user ID"),
        db: AsyncSession = Depends(get_db_session)
    ) -> ChatListResponse:
        try:
            repository = ChatRepository(db)
            if user_id:
                chats, total = await repository.get_conversations_by_user_paginated(user_id=user_id, limit=limit, offset=offset)
            else:
                chats, total = await repository.get_conversations_paginated(limit=limit, offset=offset)
            
            chat_responses = []
            for chat in chats:
                # Get messages for each chat
                chat_with_messages = await repository.get_chat_with_messages(chat.id)
                
                messages = []
                if chat_with_messages and chat_with_messages.messages:
                    messages = [
                        MessageResponse(
                            id=str(msg.id),
                            message=msg.message,
                            author=msg.author,
                            created_at=msg.created_at
                        )
                        for msg in chat_with_messages.messages
                    ]
                
                chat_responses.append(
                    ChatResponse(
                        id=str(chat.id),
                        user_id=str(chat.user_id),
                        created_at=chat.created_at,
                        updated_at=chat.updated_at,
                        messages=messages
                    )
                )
            
            return ChatListResponse(
                chats=chat_responses,
                total=total,
                limit=limit
            )
            
        except Exception as e:
            logger.error(f"Error in get_chats endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))