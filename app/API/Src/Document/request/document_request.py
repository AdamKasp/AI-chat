from pydantic import BaseModel
from typing import Optional


class DocumentSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    score_threshold: Optional[float] = None