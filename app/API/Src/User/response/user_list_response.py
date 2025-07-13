from pydantic import BaseModel, ConfigDict
from typing import List
from .user_response import UserResponse


class UserListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    users: List[UserResponse]
    total: int
    limit: int