from typing import List
import openai
from app.API.Src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def generate_embedding(self, text: str) -> List[float]:
        try:
            response = openai.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise