from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.repository.message_repository import MessageRepository
from app.API.Src.Chat.request.chat_request import ChatRequest
from app.API.Src.Tools.Technical_anwer.technical_answer_provider import TechnicalAnswerProvider
from typing import List
import logging

logger = logging.getLogger(__name__)

class CreateChatController:
    
    @staticmethod
    async def chat(
        chat_request: ChatRequest,
        db: AsyncSession = Depends(get_db_session)
    ) -> AiResponse:
        try:
            chat_repository = ChatRepository(db)
            message_repository = MessageRepository(db)
            
            # Initialize technical answer provider
            answer_provider = TechnicalAnswerProvider(db)
            
            # Handle existing conversation or create new one
            chat_history = None
            
            if chat_request.chat_id:
                # Load existing conversation
                chat_history = await chat_repository.get_chat_with_messages(chat_request.chat_id)
                if not chat_history:
                    raise HTTPException(status_code=404, detail="Chat not found")
            else:
                # Create new conversation
                chat_history = await chat_repository.create_chat(chat_request.user_id)
                logger.info(f"Created new conversation {chat_history.id}")
            
            # Generate answer using the service with automatic context retrieval
            response: AiResponse = await answer_provider.generate_answer_with_chat_context(
                user_prompt=chat_request.prompt,
                chat_id=chat_request.chat_id,
                ai_model=chat_request.model,
                rag_count=5,
                conversation_limit=10
            )
            
            # Save user message
            await message_repository.save_message(
                chat_id=chat_history.id,
                user_id=chat_request.user_id,
                message=chat_request.prompt,
                author="user"
            )
            
            # Save agent response
            await message_repository.save_message(
                chat_id=chat_history.id,
                user_id=chat_request.user_id,
                message=response.answer,
                author="agent"
            )
            
            # Add metadata to response
            response.metadata["chat_id"] = str(chat_history.id)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))