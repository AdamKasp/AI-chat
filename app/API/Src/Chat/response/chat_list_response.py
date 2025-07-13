from pydantic import BaseModel, ConfigDict
from typing import List
from .chat_response import ChatResponse


class ChatListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    chats: List[ChatResponse]
    total: int
    limit: int