from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.API.Src.Chat.models.base import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('chat_history.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    message = Column(Text, nullable=False)
    author = Column(String(10), nullable=False)  # 'user' or 'agent'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship back to chat history
    chat_history = relationship("ChatHistory", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id}, author={self.author}, message={self.message[:50]}...)>"