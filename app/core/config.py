from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FinSolve AI"
    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str
    mobile_encryption_key: str
    mobile_hash_secret: str

    embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    embedding_dimension: int = 1024

    llm_provider: str = "openrouter"
    llm_model: str
    llm_api_key: str
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
