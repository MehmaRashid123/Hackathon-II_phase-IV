"""
Configuration management for the backend application.
Loads environment variables and provides configuration settings.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str
    
    # Authentication
    BETTER_AUTH_SECRET: str
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # OpenRouter / Gemini API (for AI assistant)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "nvidia/nemotron-3-nano-30b-a3b:free"
    GEMINI_MAX_TOKENS: int = 1000
    GEMINI_TEMPERATURE: float = 0.7
    
    # MCP Server (will be added in Phase 3)
    MCP_SERVER_PORT: Optional[int] = 8001
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
