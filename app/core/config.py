from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "enterprise-ai-reference-architecture"
    log_level: str = "INFO"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.5"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_timeout_seconds: float = 30.0
    rag_chunk_size: int = 1200
    rag_chunk_overlap: int = 150

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
