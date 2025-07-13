from pydantic import BaseModel
from typing import Dict, Any


class SearchResult(BaseModel):
    id: str
    content: str
    file_path: str
    score: float
    metadata: Dict[str, Any] = {}