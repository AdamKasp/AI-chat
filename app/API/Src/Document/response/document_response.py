from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, List, Any


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    localisation: str
    content: str
    tokens: Optional[int] = None
    headers: Optional[Dict[str, List[str]]] = None
    urls: Optional[List[str]] = None
    images: Optional[List[str]] = None
    document_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_document(cls, document) -> "DocumentResponse":
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Document tokens from DB: {document.tokens}, type: {type(document.tokens)}")
        logger.info(f"Document object: {document}")
        return cls(
            id=str(document.id),
            localisation=document.localisation,
            content=document.content,
            tokens=document.tokens,
            headers=document.headers,
            urls=document.urls,
            images=document.images,
            document_metadata=document.document_metadata,
            created_at=document.created_at,
            updated_at=document.updated_at
        )