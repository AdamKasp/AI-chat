from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.Document.repository.document_repository import DocumentRepository
from app.API.Src.Document.models.document import Document
from app.API.Src.RAG.model.rag_response import RAGResponse
import logging

logger = logging.getLogger(__name__)

class NaiveRAGService:
    """
    Naive RAG (Retrieval-Augmented Generation) service that retrieves
    the most relevant documents based on user prompt using vector similarity.
    """
    
    def __init__(self, db_session: AsyncSession):
        """
        Initialize the RAG service with a database session.
        
        Args:
            db_session: Async database session for document operations
        """
        self.db_session = db_session
        self.document_repository = DocumentRepository(db_session)
    
    async def retrieve_documents(self, user_prompt: str, count: int = 5, score_threshold: float = None) -> List[Document]:
        """
        Retrieve the most relevant documents for a given user prompt.
        
        Args:
            user_prompt: The user's query/prompt
            count: Number of documents to retrieve (default: 5)
            score_threshold: Minimum similarity score threshold (optional)
            
        Returns:
            List of most relevant Document objects
        """
        try:
            logger.info(f"Starting RAG document retrieval for prompt: '{user_prompt[:50]}...'")
            
            # Use the existing vector search functionality
            documents = await self.document_repository.search_documents_by_vector(
                prompt=user_prompt,
                count=count,
                score_threshold=score_threshold
            )
            
            logger.info(f"RAG service retrieved {len(documents)} documents for prompt")
            return documents
            
        except Exception as e:
            logger.error(f"Error in RAG document retrieval: {str(e)}")
            return []
    
    async def get_context_from_documents(self, documents: List[Document]) -> str:
        """
        Extract and combine content from retrieved documents to create context.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Combined text content as context string
        """
        try:
            if not documents:
                return ""
            
            context_parts = []
            for i, doc in enumerate(documents, 1):
                # Add document metadata and content
                doc_context = f"Document {i} ({doc.localisation}):\n{doc.content}\n"
                context_parts.append(doc_context)
            
            combined_context = "\n---\n".join(context_parts)
            logger.info(f"Created context from {len(documents)} documents, total length: {len(combined_context)} characters")
            
            return combined_context
            
        except Exception as e:
            logger.error(f"Error creating context from documents: {str(e)}")
            return ""
    
    async def retrieve_and_format_context(self, user_prompt: str, count: int = 5, score_threshold: float = None) -> RAGResponse:
        """
        Complete RAG retrieval process: find documents and format as context.
        
        Args:
            user_prompt: The user's query/prompt
            count: Number of documents to retrieve (default: 5)
            score_threshold: Minimum similarity score threshold (optional)
            
        Returns:
            RAGResponse object containing documents and formatted context
        """
        try:
            # Retrieve relevant documents
            documents = await self.retrieve_documents(user_prompt, count, score_threshold)
            
            # Create formatted context
            context = await self.get_context_from_documents(documents)
            
            # Return success response
            return RAGResponse.create_success_response(
                query=user_prompt,
                documents=documents,
                context=context
            )
            
        except Exception as e:
            logger.error(f"Error in RAG retrieve_and_format_context: {str(e)}")
            return RAGResponse.create_error_response(
                query=user_prompt,
                error_message=str(e)
            )