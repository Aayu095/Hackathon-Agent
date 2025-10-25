"""
Configuration settings for the Hackathon Agent API
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Hackathon Agent API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS settings - use Field with default to avoid parsing issues
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    VERTEX_AI_LOCATION: str = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    
    # Elastic Cloud settings (Hosted deployment)
    ELASTIC_CLOUD_ID: str = os.getenv("ELASTIC_CLOUD_ID", "")
    ELASTIC_API_KEY: str = os.getenv("ELASTIC_API_KEY", "")
    
    # GitHub settings
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    
    # Elasticsearch indices
    DEVPOST_INDEX: str = "devpost_projects"
    DOCUMENTATION_INDEX: str = "hackathon_docs"
    GITHUB_INDEX: str = "github_activity"
    
    # AI Model settings
    GEMINI_MODEL: str = "gemini-pro"
    EMBEDDING_MODEL: str = "textembedding-gecko@003"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
