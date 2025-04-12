"""Configuration module for environment and settings management."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    Attributes:
        mongo_uri (str): MongoDB connection URI.
        db_name (str): Name of the MongoDB database.
        api_key (str): API key used for authentication.
        model_name (str): Hugging Face model identifier for sentiment analysis.
        log_level (str): Logging level (default: "DEBUG").
    """

    mongo_uri: str
    db_name: str
    api_key: str
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    log_level: str = "DEBUG"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance, loaded on module import
settings = Settings()
