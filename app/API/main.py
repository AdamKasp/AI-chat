from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.API.Src.Chat.chat_router import router as agent_router
from app.API.Src.Document.document_router import router as document_router
from app.API.Src.User.user_router import router as user_router
from app.API.Src.RAG.rag_router import router as rag_router
from app.API.Src.core.database.Postgres.database import init_db
from app.API.Src.core.database.Qdrant.client import qdrant_db
from app.API.Src.core.database.Qdrant.repository import QdrantRepository

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(document_router)
app.include_router(user_router)
app.include_router(rag_router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    await qdrant_db.connect()
    
    # Initialize document collection
    qdrant_repo = QdrantRepository()
    await qdrant_repo.create_collection()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("shutdown")
async def shutdown_event():
    await qdrant_db.disconnect()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
