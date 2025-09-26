from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "URL Shortener"
    debug: bool = True
    database_url: str

    class Config:
        env_file = ".env"