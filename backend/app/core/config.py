"""
Configuration management using Pydantic Settings
Singleton pattern for configuration access
"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings - Singleton pattern"""
    
    # Application
    APP_NAME: str = "Game Data Hub"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://gdh_user:gdh_password@localhost:5432/gdh_db"
    DATABASE_ECHO: bool = False
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Code Generation
    CODE_GENERATION_TEMPLATES_DIR: str = "templates"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


@lru_cache()
def get_settings() -> Settings:
    """Get settings singleton instance"""
    return Settings()

