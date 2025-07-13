from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class ChatRequest(BaseModel):
    user_id: UUID
    prompt: str
    model: str
    chat_id: Optional[UUID] = None
    system_prompt: Optional[str] = None