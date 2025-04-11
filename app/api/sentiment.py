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
    Analyze the sentiment of a review written by a user for a given product.
    The response includes a sentiment label (`positive`, `neutral`, `negative`) and a confidence score.
    The sentiment is currently predicted using a mock model,
    but the API is ready for integration with a production NLP model.
    Each result is stored in the database along with the review text and associated product ID.
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
