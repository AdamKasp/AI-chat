from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.Tools.Technical_anwer.prompt.process_chat_question_prompt import get_prompts
from app.API.Src.core.ExternalApiHelper.ai_client import completion
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse
from app.API.Src.RAG.naive_rag import NaiveRAGService
from app.API.Src.Chat.repository.message_repository import MessageRepository
from typing import List, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class TechnicalAnswerProvider:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rag_service = NaiveRAGService(db)
        self.message_repository = MessageRepository(db)
    
    async def format_conversation_history(self, messages: List) -> str:
        """Format conversation history for AI context"""
        if not messages:
            return ""
        
        formatted_history = []
        for message in messages:
            role = "User" if message.author == "user" else "Assistant"
            formatted_history.append(f"{role}: {message.message}")
        
        return "\n\nPrevious conversation:\n" + "\n".join(formatted_history) + "\n"
    
    async def get_conversation_context(self, chat_id: Optional[UUID], limit: int = 10) -> str:
        """
        Retrieve and format conversation history for a given chat
        
        Args:
            chat_id: The chat ID to retrieve history for
            limit: Maximum number of recent messages to retrieve
            
        Returns:
            Formatted conversation context string
        """
        if not chat_id:
            return ""
        
        try:
            recent_messages = await self.message_repository.get_recent_messages(chat_id, limit=limit)
            conversation_context = await self.format_conversation_history(recent_messages)
            logger.info(f"Loaded conversation history with {len(recent_messages)} messages")
            return conversation_context
        except Exception as e:
            logger.error(f"Error retrieving conversation context: {str(e)}")
            return ""
    
    async def generate_answer(
        self, 
        user_prompt: str,
        conversation_context: str = "",
        ai_model: Optional[str] = None,
        rag_count: int = 5
    ) -> AiResponse:
        """
        Generate an answer using RAG and AI model
        
        Args:
            user_prompt: The user's question
            conversation_context: Previous conversation context
            ai_model: AI model to use for generation
            rag_count: Number of documents to retrieve via RAG
            
        Returns:
            AiResponse with generated answer and metadata
        """
        try:
            # Retrieve relevant documents context using RAG
            logger.info(f"Retrieving context for prompt: '{user_prompt[:50]}...'")
            rag_response = await self.rag_service.retrieve_and_format_context(
                user_prompt=user_prompt,
                count=rag_count
            )
            
            # Combine RAG context with conversation history
            full_context = rag_response.context + conversation_context
            
            logger.info(f"RAG retrieved {rag_response.document_count} documents for context")
            
            # Generate prompts with full context
            system_prompt, prompt = get_prompts(full_context, user_prompt)
            
            # Generate response using AI
            response: AiResponse = await completion(
                system_prompt=system_prompt,
                user_prompt=prompt,
                ai_model=ai_model
            )
            
            # Add RAG metadata to response
            response.metadata["rag_info"] = {
                "documents_used": rag_response.document_count,
                "context_length": rag_response.context_length,
                "has_context": rag_response.has_context,
                "document_sources": rag_response.get_document_sources(),
                "error": rag_response.error
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating technical answer: {str(e)}")
            raise
    
    async def generate_answer_with_chat_context(
        self,
        user_prompt: str,
        chat_id: Optional[UUID] = None,
        ai_model: Optional[str] = None,
        rag_count: int = 5,
        conversation_limit: int = 10
    ) -> AiResponse:
        """
        Generate an answer with automatic conversation context retrieval
        
        Args:
            user_prompt: The user's question
            chat_id: Optional chat ID for retrieving conversation history
            ai_model: AI model to use for generation
            rag_count: Number of documents to retrieve via RAG
            conversation_limit: Maximum number of recent messages to include
            
        Returns:
            AiResponse with generated answer and metadata
        """
        # Retrieve conversation context if chat_id is provided
        conversation_context = await self.get_conversation_context(chat_id, limit=conversation_limit)
        
        # Generate answer with the retrieved context
        return await self.generate_answer(
            user_prompt=user_prompt,
            conversation_context=conversation_context,
            ai_model=ai_model,
            rag_count=rag_count
        )