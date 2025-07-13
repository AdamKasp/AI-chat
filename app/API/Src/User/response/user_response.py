from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    login: str
    created_at: datetime
    updated_at: Optional[datetime] = None