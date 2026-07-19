import sys
from functools import lru_cache

from pydantic import AnyHttpUrl, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_host: str = Field(default="0.0.0.0", description="API host", env="API_HOST")
    api_port: int = Field(default=8000, description="API port", env="API_PORT")
    log_level: str = Field(default="info", description="Log level", env="LOG_LEVEL")

    database_url: str = Field(description="Database connection URL", env="DATABASE_URL")
    redis_url: str = Field(description="Redis connection URL", env="REDIS_URL")

    aws_access_key_id: str = Field(
        description="AWS access key ID", env="AWS_ACCESS_KEY_ID"
    )
    aws_secret_access_key: str = Field(
        description="AWS secret access key", env="AWS_SECRET_ACCESS_KEY"
    )
    aws_default_region: str = Field(
        description="AWS default region", env="AWS_DEFAULT_REGION"
    )
    aws_endpoint_url: AnyHttpUrl = Field(
        description="AWS endpoint URL", env="AWS_ENDPOINT_URL"
    )
    s3_bucket_name: str = Field(description="S3 bucket name", env="S3_BUCKET_NAME")

    ollama_base_url: AnyHttpUrl = Field(
        description="Ollama base URL", env="OLLAMA_BASE_URL"
    )
    embedding_model: str = Field(description="Embedding model", env="EMBEDDING_MODEL")
    generation_model: str = Field(
        description="Generation model", env="GENERATION_MODEL"
    )

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, handling any validation errors."""
    try:
        return Settings()
    except ValidationError as e:
        print("Error loading settings:", e)
        sys.exit(1)
