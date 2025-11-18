from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Get the base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Book Management System"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db") # 'db' is the service name in docker-compose
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "book_db")

    # Construct the async PostgreSQL connection string
    # We use asyncpg driver for SQLAlchemy async operations 
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    SECRET_KEY: str = "YOUR_SECRET_KEY_MUST_BE_COMPLEX" # CHANGE THIS IN PRODUCTION
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

    # Using Ollama as the local Llama3 server URL
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://ollama:11434")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "llama3")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()