from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class VectorSearchQuery(BaseModel):
    query_vector: List[float]
    limit: int = 10
    score_threshold: Optional[float] = None
    filter_conditions: Optional[Dict[str, Any]] = None