from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from uuid import UUID




class Settings(BaseSettings):

    DATABASE_URL: str | None = None
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None

    LLM_PROVIDER: str | None = None

    LOCAL_MODEL_URL: str | None = None

    LOCAL_MODEL_NAME: str | None = None


    # ===== thêm =====
    
    AZURE_TENANT_ID: str = ""
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""

    AZURE_SEARCH_ENDPOINT: str | None = None

    AZURE_SEARCH_INDEX: str | None = None

    AZURE_SEARCH_KEY: str | None = None
    
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    
   
    GOOGLE_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    
    BOT_APP_ID: str = ""
    BOT_APP_SECRET: str = ""
    
    
    OLLAMA_MODEL: str = "gemma3:1b"
    
    SHAREPOINT_SITE_ID: str = ""
    SHAREPOINT_DRIVE_ID: str =""
    
    LOGIC_APP_URL: str 
    
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str
    MICROSOFT_REDIRECT_URI: str
    
    MAX_FILE_REVIEW: int = 5
    MIN: int = 0
    
    
    PROJECT_TRACKING_SITE_NAME: str

    PROJECT_TRACKING_LIBRARY_NAME: str
    
    EXECUTIVE_DATA_SITE_NAME: str



    EXECUTIVE_DATA_LIBRARY_NAME: str
    
    
   
    
    PROJECT_TRACKING_MODEL_ID: UUID 
    
    EXECUTIVE_DATA_MODEL_ID: UUID


    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"
    )


settings = Settings()