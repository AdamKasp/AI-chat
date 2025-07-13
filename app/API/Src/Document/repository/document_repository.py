from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.API.Src.Document.models.document import Document
from app.API.Src.core.ExternalApiHelper.OpenAI.embedding_generator import EmbeddingGenerator
from app.API.Src.core.database.Qdrant.repository import QdrantRepository
from app.API.Src.core.database.Qdrant.models import VectorDocument, VectorSearchQuery
import logging

logger = logging.getLogger(__name__)

class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_generator = EmbeddingGenerator()
        self.qdrant_repo = QdrantRepository()
    
    async def save_document(self, document: Document, file_path: str = None) -> Document:
        """
        Save a Document object to both PostgreSQL and Qdrant databases.
        
        Args:
            document: Document object to save
            file_path: Original file path for vector storage metadata
            
        Returns:
            Saved Document object with updated ID and timestamps
        """
        try:
            # Save to PostgreSQL first
            self.session.add(document)
            await self.session.commit()
            await self.session.refresh(document)
            
            # Generate embedding and save to Qdrant
            embedding = await self.embedding_generator.generate_embedding(document.content)
            
            # Create summary from content (first 50 characters) - temporary solution, will be replaced with API summarization
            summary = document.content[:50] + "..." if len(document.content) > 50 else document.content
            
            # Create vector document for Qdrant
            vector_doc = VectorDocument.from_document(
                str(document.id),
                summary
            )
            
            # Save to Qdrant
            await self.qdrant_repo.upsert_document(vector_doc, embedding)
            
            logger.info(f"Successfully saved document {document.id} to both PostgreSQL and Qdrant")
            return document
            
        except Exception as e:
            # Rollback PostgreSQL transaction in case of error
            await self.session.rollback()
            logger.error(f"Error saving document: {str(e)}")
            raise
    
    async def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        result = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()
    
    async def get_documents_paginated(self, limit: int = 100, offset: int = 0) -> Tuple[List[Document], int]:
        # Get total count
        count_result = await self.session.execute(
            select(func.count(Document.id))
        )
        total = count_result.scalar()
        
        # Get paginated results
        result = await self.session.execute(
            select(Document)
            .order_by(Document.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all(), total
    
    async def search_documents_by_vector(self, prompt: str, count: int, score_threshold: Optional[float] = None) -> List[Document]:
        """
        Search documents in the database based on vector similarity.
        
        Args:
            prompt: Query text to generate embedding
            count: Maximum number of results to return
            score_threshold: Minimum similarity threshold (optional)
            
        Returns:
            List of documents sorted by similarity
        """
        try:
            # 1. Generate embedding from prompt
            query_embedding = await self.embedding_generator.generate_embedding(prompt)
            logger.info(f"Generated embedding for search prompt: '{prompt[:50]}...'")
            
            # 2. Prepare query for Qdrant
            search_query = VectorSearchQuery(
                query_vector=query_embedding,
                limit=count,
                score_threshold=score_threshold
            )
            
            # 3. Execute search in Qdrant
            search_results = await self.qdrant_repo.search_similar(search_query)
            logger.info(f"Found {len(search_results)} results from Qdrant search")
            
            if not search_results:
                logger.info("No results found in vector search")
                return []
            
            # 4. Retrieve full documents from PostgreSQL
            documents = []
            for result in search_results:
                try:
                    # Convert ID from string to UUID
                    document_id = UUID(result.id)
                    document = await self.get_document_by_id(document_id)
                    
                    if document:
                        documents.append(document)
                        logger.debug(f"Retrieved document {document_id} with score {result.score}")
                    else:
                        logger.warning(f"Document {document_id} not found in PostgreSQL")
                        
                except ValueError as e:
                    logger.error(f"Invalid UUID format for document ID {result.id}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Error retrieving document {result.id}: {e}")
                    continue
            
            logger.info(f"Successfully retrieved {len(documents)} documents for search query")
            return documents
            
        except Exception as e:
            logger.error(f"Error in vector search for prompt '{prompt}': {str(e)}")
            return []
    
    async def delete_document(self, document_id: UUID) -> bool:
        """
        Delete document from both databases: PostgreSQL and Qdrant.
        
        Args:
            document_id: UUID of document to delete
            
        Returns:
            True if document was deleted, False otherwise
        """
        try:
            # 1. Check if document exists in PostgreSQL
            document = await self.get_document_by_id(document_id)
            if not document:
                logger.warning(f"Document {document_id} not found in PostgreSQL")
                return False
            
            # 2. Delete from Qdrant
            try:
                await self.qdrant_repo.delete_document(str(document_id))
                logger.info(f"Successfully deleted document {document_id} from Qdrant")
            except Exception as e:
                logger.error(f"Error deleting document {document_id} from Qdrant: {str(e)}")
                # Continue with PostgreSQL deletion even if Qdrant fails
            
            # 3. Delete from PostgreSQL
            await self.session.delete(document)
            await self.session.commit()
            
            logger.info(f"Successfully deleted document {document_id} from both databases")
            return True
            
        except Exception as e:
            # Rollback PostgreSQL transaction in case of error
            await self.session.rollback()
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False