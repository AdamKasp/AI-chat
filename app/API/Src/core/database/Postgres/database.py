from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.API.Src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    from app.API.Src.Chat.models.base import Base as ChatBase
    from app.API.Src.Chat.models.chat_history import ChatHistory  # Import to register model
    from app.API.Src.Chat.models.message import Message  # Import to register model
    from app.API.Src.Document.models.document import Base as DocumentBase
    from app.API.Src.User.models.user import Base as UserBase
    async with engine.begin() as conn:
        await conn.run_sync(ChatBase.metadata.create_all)
        await conn.run_sync(DocumentBase.metadata.create_all)
        await conn.run_sync(UserBase.metadata.create_all)