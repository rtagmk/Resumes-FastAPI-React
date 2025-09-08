"""
Module for application settings and configuration using pydantic-settings.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.
    """

    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "db"
    db_port: str = "5432"
    db_name: str = "resumes"
    db_dialect_async: str = "postgresql+asyncpg"
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def database_url_async(self) -> str:
        """
        Dynamically construct the database async URL.
        """
        return (
            f"{self.db_dialect_async}://"
            f"{self.db_user}:{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )


settings: Settings = Settings()
