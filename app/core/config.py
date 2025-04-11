"""App settings management using pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.

    Attributes:
        mongo_uri (str): MongoDB connection URI.
        db_name (str): Name of the MongoDB database.
        api_key (str): API key for authentication (to be used in headers).
    """

    mongo_uri: str
    db_name: str
    api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance, loaded on module import
settings = Settings()
