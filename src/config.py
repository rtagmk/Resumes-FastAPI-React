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

    db_user: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: str = ""
    db_name: str = ""
    db_dialect_async: str = ""
    secret_key: str = ""
    algorithm: str = ""
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
