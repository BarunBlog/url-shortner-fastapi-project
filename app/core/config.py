from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the application."""
    PORT: int = 8000
    MONGO_URI: str
    BASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()