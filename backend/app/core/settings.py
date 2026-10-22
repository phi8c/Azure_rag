from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from uuid import UUID




class Settings(BaseSettings):

    DATABASE_URL: str | None = None
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = None



    # ===== thêm =====
    
    AZURE_TENANT_ID: str = ""
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""

    AZURE_SEARCH_ENDPOINT: str | None = None

    AZURE_SEARCH_INDEX: str | None = None

    AZURE_SEARCH_KEY: str | None = None

    # Ngưỡng cosine tối thiểu để chunk được coi là liên quan (dưới ngưỡng thì không đưa vào context/sources)
    CHAT_MIN_SIMILARITY: float = 0.44
    
    
    
   
    
    BOT_APP_ID: str = ""
    BOT_APP_SECRET: str = ""
    
    
    
    SHAREPOINT_SITE_ID: str = ""
    SHAREPOINT_DRIVE_ID: str =""
    
    LOGIC_APP_URL: str 
    
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_API_VERSION: str = ""
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = ""
    CLAUDE_API_KEY: str = ""
    CLAUDE_WORKSPACE_ID: str = ""
    CLAUDE_SONNET_MODEL: str = "claude-sonnet-5-5"
    CLAUDE_HAIKU_MODEL: str = "claude-haiku-5-5"
    MICROSOFT_REDIRECT_URI: str
    
    MAX_FILE_REVIEW: int = 5
    MIN: int = 0
    
    
    PROJECT_TRACKING_SITE_NAME: str

    PROJECT_TRACKING_LIBRARY_NAME: str
    
    EXECUTIVE_DATA_SITE_NAME: str



    EXECUTIVE_DATA_LIBRARY_NAME: str
    
    
   
    
    PROJECT_TRACKING_MODEL_ID: UUID 
    
    EXECUTIVE_DATA_MODEL_ID: UUID
    
    
    
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: str
    AZURE_DOCUMENT_INTELLIGENCE_KEY: str


    # Kho pháp luật trên Azure (Search metadata + Blob toàn văn)
    AZURE_LEGAL_SEARCH_INDEX: str | None = None
    AZURE_LEGAL_BLOB_CONTAINER: str | None = None
    AZURE_STORAGE_ACCOUNT_URL: str | None = None
    AZURE_STORAGE_SAS_TOKEN: str | None = None
    AZURE_STORAGE_KEY: str | None = None
    
    
    GOOGLE_CUSTOMER_ID: str
    GOOGLE_CUSTOMER_SECRET: str


    GOOGLE_REDIRECT_URI: str
    
    MEETING_SYNC_USER_ID: str
    
   

    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"
    )


settings = Settings()
