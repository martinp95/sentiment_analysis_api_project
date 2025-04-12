"""Pydantic model for health check response."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Output model for health check response.

    Attributes:
        status (str): Health status of the service.
    """

    status: str = Field(..., example="healthy", description="API status indicator.")
