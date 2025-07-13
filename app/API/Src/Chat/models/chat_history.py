from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.API.Src.Chat.models.base import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to messages
    messages = relationship("Message", back_populates="chat_history", cascade="all, delete-orphan", order_by="Message.created_at")
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"