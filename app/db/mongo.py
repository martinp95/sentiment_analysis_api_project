"""MongoDB client factory using Motor."""

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


def get_mongo_client() -> AsyncIOMotorClient:
    """
    Create and return a MongoDB client instance.

    Returns:
        AsyncIOMotorClient: An asynchronous MongoDB client.
    """
    return AsyncIOMotorClient(settings.mongo_uri)
