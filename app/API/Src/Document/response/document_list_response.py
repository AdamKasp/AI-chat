from pydantic import BaseModel, ConfigDict
from typing import List
from .document_response import DocumentResponse


class DocumentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    documents: List[DocumentResponse]
    total: int
    limit: int