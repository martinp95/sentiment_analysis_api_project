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
    summary="Analyze the sentiment of a product review",
    description="""
Analyze the **sentiment** of a product review and store the result in the database.

### Input:
- `review` (string): The textual content of the review
- `product_id` (string): The ID of the product being reviewed

### Output:
- `sentiment`: One of `"positive"`, `"neutral"`, or `"negative"`
- `confidence`: A float between `0.0` and `1.0` representing prediction certainty

### Notes:
- The sentiment prediction is powered by a real transformer-based model (`DistilBERT`)
- Reviews and predictions are stored in the database for later analysis
- Authentication via API key (`X-API-Key`) is required
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

    Returns:
        ReviewResponse: The predicted sentiment and confidence score.

    Raises:
        HTTPException (400): If the review text is empty.
    """
    if not payload.review.strip():
        raise bad_request_exception("Review text cannot be empty.")

    return await analyze_and_store_sentiment(payload)
