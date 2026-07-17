from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "info"

    database_url: str
    redis_url: str

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    aws_endpoint_url: str
    s3_bucket_name: str

    ollama_base_url: str
    embedding_model: str
    generation_model: str

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


try:
    settings = Settings()
except ValidationError:
    raise RuntimeError("Error loading settings")
