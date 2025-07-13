from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
import logging

from app.API.Src.core.config import settings

logger = logging.getLogger(__name__)

class QdrantDatabase:
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        
    async def connect(self) -> None:
        try:
            self.client = QdrantClient(url=settings.QDRANT_URL)
            logger.info(f"Connected to Qdrant at {settings.QDRANT_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    
    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Disconnected from Qdrant")
    
    def get_client(self) -> QdrantClient:
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call connect() first.")
        return self.client

qdrant_db = QdrantDatabase()