from sqlalchemy import Column, String, DateTime, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid
from typing import Dict, List, Optional

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    localisation = Column(String(500), nullable=False)  # File path in Corpus
    content = Column(Text, nullable=False)
    tokens = Column(Integer, nullable=True)  # Number of tokens in document
    headers = Column(JSON, nullable=True)  # Extracted headers from document
    urls = Column(JSON, nullable=True)  # List of URLs found in document
    images = Column(JSON, nullable=True)  # List of images found in document
    document_metadata = Column(JSON, nullable=True)  # Additional metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, content: str = None, metadata: Dict = None, **kwargs):
        """Initialize Document with content and metadata from text splitter."""
        if content is not None:
            self.content = content
        if metadata is not None:
            self.tokens = metadata.get('tokens')
            self.headers = metadata.get('headers')
            self.urls = metadata.get('urls')
            self.images = metadata.get('images')
            # Store any additional metadata
            self.document_metadata = {k: v for k, v in metadata.items() 
                           if k not in ['tokens', 'headers', 'urls', 'images']}
        # Handle any additional kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"<Document(id={self.id}, localisation={self.localisation[:50] if self.localisation else 'None'}...)>"