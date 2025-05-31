from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field


class Settings(BaseSettings):
    """Settings for the application.

    This class is used to store the settings for the application.
    """

    PROJECT_NAME: str = "HireWise.ai"
    API_V1_STR: str = "/v1"
    PROJECT_DESCRIPTION: str = "API for HireWise.ai"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_LICENSE: str = "Proprietary"
    PROJECT_LICENSE_URL: str = "https://hirewise.ai/license"
    PROJECT_URL: str = "https://hirewise.ai"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Local development
        "https://*.hirewise.ai",  # Production
        "https://hirewise.ai",  # Production domain
        "https://*.fly.dev",  # Production domain
    ]  # noqa: E501

    # Security
    JWT_SECRET: str = Field(default="", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = Field(default="", description="Database URL")
    DIRECT_URL: str = Field(default="", description="Direct database URL")

    # API Keys
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")

    # Vector database settings
    VECTOR_DIMENSION: int = 384  # all-MiniLM-L6-v2 dimension

    # LLM settings
    LLM_MODEL: str = Field(default="gpt-4o", description="LLM model to use")
    LLM_TEMPERATURE: float = 0.0

    # Document processing
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Crawling settings
    MAX_URLS_PER_PROJECT: int = 100
    MAX_WORKERS: int = 5

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
