from app.API.Src.Chat.prompt.process_chat_question_prompt import get_prompts
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.core.ExternalApiHelper.ai_client import completion
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.repository.message_repository import MessageRepository
from app.API.Src.Chat.request.chat_request import ChatRequest
from app.API.Src.RAG.naive_rag import NaiveRAGService
from typing import List
import logging

logger = logging.getLogger(__name__)

class CreateChatController:
    @staticmethod
    async def _format_conversation_history(messages: List) -> str:
        """Format conversation history for AI context"""
        if not messages:
            return ""
        
        formatted_history = []
        for message in messages:
            role = "User" if message.author == "user" else "Assistant"
            formatted_history.append(f"{role}: {message.message}")
        
        return "\n\nPrevious conversation:\n" + "\n".join(formatted_history) + "\n"
    
    @staticmethod
    async def chat(
        chat_request: ChatRequest,
        db: AsyncSession = Depends(get_db_session)
    ) -> AiResponse:
        try:
            chat_repository = ChatRepository(db)
            message_repository = MessageRepository(db)
            
            # Handle existing conversation or create new one
            chat_history = None
            conversation_context = ""
            
            if chat_request.chat_id:
                # Load existing conversation
                chat_history = await chat_repository.get_chat_with_messages(chat_request.chat_id)
                if not chat_history:
                    raise HTTPException(status_code=404, detail="Chat not found")
                
                # Format conversation history for context
                recent_messages = await message_repository.get_recent_messages(chat_request.chat_id, limit=10)
                conversation_context = await CreateChatController._format_conversation_history(recent_messages)
                logger.info(f"Loaded conversation history with {len(recent_messages)} messages")
            else:
                # Create new conversation
                chat_history = await chat_repository.create_chat(chat_request.user_id)
                logger.info(f"Created new conversation {chat_history.id}")
            
            # Initialize RAG service
            rag_service = NaiveRAGService(db)
            
            # Retrieve relevant documents context using RAG
            logger.info(f"Retrieving context for chat prompt: '{chat_request.prompt[:50]}...'")
            rag_response = await rag_service.retrieve_and_format_context(
                user_prompt=chat_request.prompt,
                count=5  # Get top 5 most relevant documents
            )
            
            # Combine RAG context with conversation history
            full_context = rag_response.context + conversation_context
            
            logger.info(f"RAG retrieved {rag_response.document_count} documents for context")
            
            # Generate prompts with full context
            system_prompt, prompt = get_prompts(full_context, chat_request.prompt)
        
            response: AiResponse = await completion(
                system_prompt=system_prompt,
                user_prompt=prompt,
                ai_model=chat_request.model
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
            response.metadata["rag_info"] = {
                "documents_used": rag_response.document_count,
                "context_length": rag_response.context_length,
                "has_context": rag_response.has_context,
                "document_sources": rag_response.get_document_sources(),
                "error": rag_response.error
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))