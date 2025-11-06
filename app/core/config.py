from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration settings for the application."""
    PORT: int = 8000
    BASE_URL: str

    MONGO_URI: str

    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASS: str
    PG_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()