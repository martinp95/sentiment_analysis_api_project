"""Custom HTTP exceptions and error response model."""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Generic error response returned by the API.
    """

    detail: str = Field(..., example="Unauthorized access")


def unauthorized_exception(detail: str = "Invalid or missing API key") -> HTTPException:
    """
    Raise a 401 Unauthorized exception with a custom error message.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def not_found_exception(resource: str = "Resource") -> HTTPException:
    """
    Raise a 404 Not Found exception with a custom error message.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found",
    )


def bad_request_exception(detail: str = "Bad request") -> HTTPException:
    """
    Raise a 400 Bad Request exception with a custom error message.
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )
