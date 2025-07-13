from fastapi import APIRouter, Depends, Query, UploadFile, File
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.API.Src.core.database.Postgres.database import get_db_session
from app.API.Src.Document.controller.upload_document import UploadDocumentController
from app.API.Src.Document.controller.get_document_list import GetDocumentListController
from app.API.Src.Document.controller.get_document import GetDocumentController
from app.API.Src.Document.controller.delete_document import DeleteDocumentController
from app.API.Src.Document.response.document_upload_response import DocumentUploadResponse
from app.API.Src.Document.response.document_list_response import DocumentListResponse
from app.API.Src.Document.response.document_response import DocumentResponse

router = APIRouter()

@router.post("/documents", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db_session)):
    return await UploadDocumentController.upload_document(file, db)

@router.get("/documents", response_model=DocumentListResponse, tags=["Documents"])
async def get_documents(limit: int = Query(default=100, le=1000), offset: int = Query(default=0, ge=0), db: AsyncSession = Depends(get_db_session)):
    return await GetDocumentListController.get_documents(limit, offset, db)


@router.get("/documents/{document_id}", response_model=DocumentResponse, tags=["Documents"])
async def get_document(document_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await GetDocumentController.get_document(document_id, db)

@router.delete("/documents/{document_id}", response_model=dict, tags=["Documents"])
async def delete_document(document_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await DeleteDocumentController.delete_document(document_id, db)