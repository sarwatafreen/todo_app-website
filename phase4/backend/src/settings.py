from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_audience: Optional[str] = None
    jwt_issuer: Optional[str] = None
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str
    openai_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()