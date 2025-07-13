from pydantic import BaseModel
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    id: str
    localisation: str
    message: str
    created_at: datetime