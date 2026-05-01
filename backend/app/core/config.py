from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "StockRL API"
    debug: bool = False
    # Base de datos PostgreSQL
    database_url: str = "postgresql://postgres:postgres@localhost:5432/stockai"
    # JWT
    secret_key: str = "cambiar-en-produccion-secret-key-muy-segura"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480  # 8 horas

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
