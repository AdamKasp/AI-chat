from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AiResponse(BaseModel):
    finishReason: str
    answer: str
    metadata: Dict[str, Any]
