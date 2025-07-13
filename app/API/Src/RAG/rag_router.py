from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.RAG.naive_rag import NaiveRAGService
from app.API.Src.RAG.model.rag_response import RAGResponse
from app.API.Src.Document.response.document_response import DocumentResponse

router = APIRouter()

@router.get("/rag/search", response_model=dict, tags=["RAG"])
async def rag_search(
    prompt: str = Query(..., description="User prompt for document retrieval"),
    count: int = Query(default=5, le=20, description="Number of documents to retrieve"),
    score_threshold: Optional[float] = Query(default=None, description="Minimum similarity score"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    RAG (Retrieval-Augmented Generation) endpoint that retrieves the most relevant documents
    for a given user prompt using vector similarity search.
    Endpoint mostly for testing purposes, use chat endpoint for production.
    """
    rag_service = NaiveRAGService(db)
    rag_response = await rag_service.retrieve_and_format_context(prompt, count, score_threshold)
    
    # Convert documents to response format
    document_responses = [
        DocumentResponse.from_document(doc) for doc in rag_response.documents
    ]
    
    return {
        "query": rag_response.query,
        "document_count": rag_response.document_count,
        "documents": document_responses,
        "context": rag_response.context,
        "context_length": rag_response.context_length,
        "has_context": rag_response.has_context,
        "document_sources": rag_response.get_document_sources(),
        "error": rag_response.error
    }