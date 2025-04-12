"""Health check endpoint for the API."""

from fastapi import APIRouter

from app.models.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check for API availability",
    description="""
Returns the health status of the API.

Useful for:
- Readiness/liveness checks in production
- Monitoring from orchestrators (e.g., Kubernetes)

### Response:
``` json
{
"status": "healthy"
}
```

This endpoint does not require authentication.""",
)
async def health_check():
    """
    Returns a simple confirmation that the API is up and running.
    """
    return HealthResponse(status="healthy")
