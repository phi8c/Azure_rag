from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    DATABASE_URL: str | None = None
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None

    LLM_PROVIDER: str | None = None

    LOCAL_MODEL_URL: str | None = None

    LOCAL_MODEL_NAME: str | None = None


    # ===== thêm =====

    AZURE_SEARCH_ENDPOINT: str | None = None

    AZURE_SEARCH_INDEX: str | None = None

    AZURE_SEARCH_KEY: str | None = None
    
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    
    OLLAMA_MODEL: str = "gemma3:1b"


    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"
    )


settings = Settings()