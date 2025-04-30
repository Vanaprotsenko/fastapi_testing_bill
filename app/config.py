import os
from pydantic_settings import BaseSettings
from typing import Any, Dict, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Receipt API"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/receipt_db")

    DEFAULT_RECEIPT_LINE_WIDTH: int = 32

    class Config:
        case_sensitive = True


settings = Settings()