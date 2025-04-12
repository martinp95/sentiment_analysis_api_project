"""API route for sentiment analysis."""

from fastapi import APIRouter, Depends, status

from app.core.exceptions import ErrorResponse, bad_request_exception
from app.core.security import verify_api_key
from app.models.review import ReviewRequest, ReviewResponse
from app.services.sentiment import analyze_and_store_sentiment

router = APIRouter()


@router.post(
    "/reviews/sentiment",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Sentiment"],
    summary="Analyze sentiment of a product review",
    description="""
Analyze the **sentiment** of a product review and store the result.

**Returns:**
- `sentiment`: `positive`, `neutral`, or `negative`
- `confidence`: float (between 0.0 and 1.0)

**Notes:**
- The prediction is currently based on a mock model.
- Results are stored in the database with review text and product ID.
- Requires authentication via API key (`X-API-Key`).
""",
    responses={
        201: {"description": "Sentiment successfully analyzed and saved."},
        400: {
            "model": ErrorResponse,
            "description": "The review field is empty or invalid.",
        },
        401: {"model": ErrorResponse, "description": "Missing or invalid API key."},
    },
    dependencies=[Depends(verify_api_key)],
)
async def predict_sentiment(payload: ReviewRequest) -> ReviewResponse:
    """
    Analyze the sentiment of a review and store the result in the database.

    Args:
        payload (ReviewRequest): The review content and product ID.
        request (Request): FastAPI request object to access app state.

    Returns:
        ReviewResponse: The predicted sentiment and confidence score.

    Raises:
        HTTPException (400): If the review text is empty.
    """
    if not payload.review.strip():
        raise bad_request_exception("Review text cannot be empty.")

    return await analyze_and_store_sentiment(payload)
