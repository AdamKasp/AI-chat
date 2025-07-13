from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Docker specific
    CONTAINER_NAME: str = "ai-agent"
    
    # Database configuration
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "ai_agent_db"
    DB_USER: str = "ai_agent"
    DB_PASSWORD: str = "ai_agent_password"
    
    # Document storage
    CORPUS_PATH: str = Field(default="./Corpus", env="CORPUS_PATH")
    
    # Qdrant configuration
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: int = 6334
    VECTOR_SIZE: int = 1536  # OpenAI embedding size
    
    # Document processing
    DOCUMENT_TOKEN_LIMIT: int = Field(default=500, env="DOCUMENT_TOKEN_LIMIT")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def corpus_absolute_path(self) -> Path:
        return Path(self.CORPUS_PATH).resolve()
    
    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    class Config:
        env_file = ".env"


settings = Settings()
