from typing import List, Optional
from pydantic import BaseModel, Field
from app.API.Src.Document.models.document import Document


class RAGResponse(BaseModel):
    """
    Model representing the response from RAG (Retrieval-Augmented Generation) service.
    Contains retrieved documents, formatted context, and metadata about the retrieval process.
    """
    
    query: str = Field(..., description="Original user query/prompt")
    documents: List[Document] = Field(default_factory=list, description="Retrieved documents from vector search")
    context: str = Field(default="", description="Formatted context string from documents")
    document_count: int = Field(default=0, description="Number of documents retrieved")
    error: Optional[str] = Field(default=None, description="Error message if retrieval failed")
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        arbitrary_types_allowed = True  # Allow SQLAlchemy models
        json_encoders = {
            # Custom encoder for Document objects if needed
        }
    
    @property
    def has_context(self) -> bool:
        """Check if any meaningful context was retrieved"""
        return bool(self.context.strip())
    
    @property
    def has_error(self) -> bool:
        """Check if there was an error during retrieval"""
        return self.error is not None
    
    @property
    def context_length(self) -> int:
        """Get the length of the context string"""
        return len(self.context)
    
    def get_document_ids(self) -> List[str]:
        """Get list of document IDs that were retrieved"""
        return [str(doc.id) for doc in self.documents]
    
    def get_document_sources(self) -> List[str]:
        """Get list of document source locations/filenames"""
        return [doc.localisation for doc in self.documents]
    
    @classmethod
    def create_success_response(
        cls, 
        query: str, 
        documents: List[Document], 
        context: str
    ) -> "RAGResponse":
        """Create a successful RAG response"""
        return cls(
            query=query,
            documents=documents,
            context=context,
            document_count=len(documents),
            error=None
        )
    
    @classmethod
    def create_error_response(cls, query: str, error_message: str) -> "RAGResponse":
        """Create an error RAG response"""
        return cls(
            query=query,
            documents=[],
            context="",
            document_count=0,
            error=error_message
        )