"""API route for fwtching product-level sentiment stats."""

from fastapi import APIRouter, Depends, Path, status

from app.core.exceptions import ErrorResponse
from app.core.security import verify_api_key
from app.models.stats import SentimentStatsResponse
from app.services.stats import compute_sentiment_stats_by_product

router = APIRouter()


@router.get(
    "/reviews/stats/{product_id}",
    response_model=SentimentStatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get sentiment stats by product",
    tags=["Sentiment"],
    description="""
    Retrieve the sentiment distribution (positive/neutral/negative)
    for all reviews associated with a given product.
    """,
    responses={
        200: {"description": "Statistics successfully retrieved."},
        404: {
            "model": ErrorResponse,
            "description": "No reviews found for this product.",
        },
    },
    dependencies=[Depends(verify_api_key)],
)
async def get_stats(
    product_id: str = Path(..., description="ID of the product to fetch stats for")
) -> SentimentStatsResponse:
    """
    Get sentiment distribution (positive/neutral/negative) for a given product.

    Args:
        request (Request): FastAPI request object.
        product_id (str): ID of the product.

    Returns:
        SentimentStatsResponse: Stats grouped by sentiment label.

    Raises:
        404: If no reviews are found for the given product.
    """
    return await compute_sentiment_stats_by_product(product_id)
