from fastapi import APIRouter, Depends, Query
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Chat.controller.create_chat import CreateChatController
from app.API.Src.Chat.controller.get_chat_list import GetChatListController
from app.API.Src.Chat.controller.get_chat import GetChatController
from app.API.Src.Chat.request.chat_request import ChatRequest
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse
from app.API.Src.Chat.response.chat_list_response import ChatListResponse
from app.API.Src.Chat.response.chat_response import ChatResponse

router = APIRouter()

@router.post("/chat", response_model=AiResponse, tags=["Chat"])
async def chat(chat_request: ChatRequest, db: AsyncSession = Depends(get_db_session)):
    return await CreateChatController.chat(chat_request, db)

@router.get("/chats", response_model=ChatListResponse, tags=["Chat"])
async def get_chats(limit: int = Query(default=100, le=1000), offset: int = Query(default=0, ge=0), user_id: Optional[UUID] = Query(default=None, description="Filter chats by user ID"), db: AsyncSession = Depends(get_db_session)):
    return await GetChatListController.get_chats(limit, offset, user_id, db)

@router.get("/chats/{chat_id}", response_model=ChatResponse, tags=["Chat"])
async def get_chat(chat_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await GetChatController.get_chat(chat_id, db)