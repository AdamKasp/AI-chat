from typing import List, Optional
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import logging

from .client import qdrant_db
from .models import VectorDocument, SearchResult, VectorSearchQuery
from app.API.Src.core.config import settings

logger = logging.getLogger(__name__)


class QdrantRepository:
    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name
        self.vector_size = settings.VECTOR_SIZE
    
    async def create_collection(self) -> bool:
        try:
            client = qdrant_db.get_client()
            
            # Check if collection exists
            collections = client.get_collections()
            if any(col.name == self.collection_name for col in collections.collections):
                logger.info(f"Collection '{self.collection_name}' already exists")
                return True
            
            # Create collection
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection '{self.collection_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return False
    
    async def upsert_document(self, document: VectorDocument, vector: List[float]) -> bool:
        try:
            client = qdrant_db.get_client()
            
            payload = {
                "summary": document.summary,
                **document.metadata
            }
            
            client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=document.id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )
            logger.info(f"Upserted document {document.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upsert document: {e}")
            return False
    
    async def search_similar(self, query: VectorSearchQuery) -> List[SearchResult]:
        try:
            client = qdrant_db.get_client()
            
            search_result = client.search(
                collection_name=self.collection_name,
                query_vector=query.query_vector,
                limit=query.limit,
                score_threshold=query.score_threshold,
                query_filter=models.Filter(**query.filter_conditions) if query.filter_conditions else None,
                with_payload=True
            )
            
            results = []
            for point in search_result:
                result = SearchResult(
                    id=str(point.id),
                    content=point.payload.get("summary", ""),
                    file_path="",  # No longer stored
                    score=point.score,
                    metadata={k: v for k, v in point.payload.items() 
                             if k not in ["summary"]}
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        try:
            client = qdrant_db.get_client()
            
            client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[document_id]
                )
            )
            logger.info(f"Deleted document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False
    
    async def get_collection_info(self) -> dict:
        try:
            client = qdrant_db.get_client()
            info = client.get_collection(self.collection_name)
            return {
                "name": info.config.params.vectors.size,
                "vectors_count": info.vectors_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "points_count": info.points_count
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}