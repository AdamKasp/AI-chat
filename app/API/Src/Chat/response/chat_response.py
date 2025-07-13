from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    message: str
    author: str
    created_at: datetime


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[MessageResponse] = []
    
    # For backward compatibility - get last user message and last agent response
    @property
    def last_user_message(self) -> Optional[str]:
        user_messages = [msg.message for msg in self.messages if msg.author == "user"]
        return user_messages[-1] if user_messages else None
    
    @property
    def last_agent_response(self) -> Optional[str]:
        agent_messages = [msg.message for msg in self.messages if msg.author == "agent"]
        return agent_messages[-1] if agent_messages else None