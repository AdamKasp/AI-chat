from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.ExternalApiHelper.ai_client import completion
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.response.chat_response import ChatResponse
from app.API.Src.Chat.response.chat_list_response import ChatListResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=AiResponse, tags=["Chat"])
async def chat(
    prompt: str, 
    model: str,
    system_prompt: str = None,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        response: AiResponse = await completion(
            system_prompt=system_prompt,
            user_prompt=prompt,
            ai_model=model
        )
        
        try:
            repository = ChatRepository(db)
            saved_conversation = await repository.save_conversation(
                prompt=prompt,
                answer=response.answer
            )
            
            response.metadata["conversation_id"] = str(saved_conversation.id)
            
        except Exception as e:
            logger.error(f"Failed to save conversation to database: {str(e)}")
            
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chats", response_model=ChatListResponse, tags=["Chat"])
async def get_chats(
    limit: int = Query(default=100, le=1000),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = ChatRepository(db)
        chats, total = await repository.get_conversations_paginated(limit=limit, offset=offset)
        
        chat_responses = [
            ChatResponse(
                id=str(chat.id),
                prompt=chat.prompt,
                answer=chat.answer,
                created_at=chat.created_at
            )
            for chat in chats
        ]
        
        return ChatListResponse(
            chats=chat_responses,
            total=total,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error in get_chats endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chats/{chat_id}", response_model=ChatResponse, tags=["Chat"])
async def get_chat(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        repository = ChatRepository(db)
        chat = await repository.get_conversation_by_id(chat_id)
        
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        return ChatResponse(
            id=str(chat.id),
            prompt=chat.prompt,
            answer=chat.answer,
            created_at=chat.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))