from pydantic import BaseModel
from typing import Dict, Any


class VectorDocument(BaseModel):
    id: str
    summary: str
    metadata: Dict[str, Any] = {}
    
    @classmethod
    def from_document(cls, document_id: str, summary: str, **metadata) -> "VectorDocument":
        return cls(
            id=document_id,
            summary=summary,
            metadata=metadata
        )