from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class DefaultSettings(BaseSettings):
    """Base settings class that all other settings inherit from."""
    model_config = SettingsConfigDict(
        env_file=".env",           # Read from .env file
        extra="ignore",            # Don't error on unknown env variables
        frozen=True,               # Make settings immutable (can't change after creation)
        env_nested_delimiter="__", # Allow nested settings like POSTGRES__DATABASE_URL
    )

class Settings(DefaultSettings):
    """Main application settings - this is your app's configuration."""
    
    # Basic app info
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"
    service_name: str = "rag-api"

    # PostgreSQL configuration - where your data lives
    postgres_database_url: str = "postgresql://rag_user:rag_password@localhost:5432/rag_db" # point to your Postgres DB defined in compose.yml
    postgres_echo_sql: bool = False        # Set to True to see SQL queries in logs
    postgres_pool_size: int = 20           # How many connections to keep open
    postgres_max_overflow: int = 0         # Additional connections when pool is full

    # OpenSearch configuration - for search functionality (future)
    # opensearch_host: str = "http://opensearch:9200"

    # # Ollama configuration - for AI functionality (future)
    # ollama_host: str = "http://ollama:11434"
    # ollama_models: List[str] = Field(default=["gpt-oss:20b", "llama3.2:1b"])
    # ollama_default_model: str = "llama3.2:1b"
    # ollama_timeout: int = 300  # 5 minutes for large model operations

    # @field_validator("ollama_models", mode="before")
    # @classmethod
    # def parse_ollama_models(cls, v):
    #     """Convert comma-separated string to list of models."""
    #     if isinstance(v, str):
    #         return [model.strip() for model in v.split(",") if model.strip()]
    #     return v


def get_settings() -> Settings:
    """Factory function to create settings instance."""
    return Settings()