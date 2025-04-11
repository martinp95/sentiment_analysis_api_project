"""API Key authentication system for route protection."""

from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings
from app.core.exceptions import unauthorized_exception

# Name of the header clients must use to send the API key
API_KEY_NAME = "X-API-Key"

# Dependency extractor from FastAPI's APIKeyHeader
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependency to enforce API key authentication.

    Args:
        api_key (str): The API key from the request header.

    Returns:
        str: The API key if valid.

    Raises:
        HTTPException: If API key is missing or invalid.
    """
    if not api_key or api_key != settings.api_key:
        raise unauthorized_exception("Invalid or missing API key.")
    return api_key
