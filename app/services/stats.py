"""Service layer for computing sentiment statistics."""

from app.core.context import context
from app.core.exceptions import not_found_exception
from app.models.stats import SentimentStatsResponse
from app.repositories.stats_repository import fetch_sentiment_distribution_by_product


async def compute_sentiment_stats_by_product(product_id: str) -> SentimentStatsResponse:
    """
    Compute sentiment stats for a specific product.

    Args:
        product_id (str): Product identifier.

    Returns:
        SentimentStatsResponse: Aggregated sentiment distribution.

    Raises:
        HTTPException: If no reviews are found for the product.
    """
    db = context.get_db()  # Get the MongoDB database instance

    stats = await fetch_sentiment_distribution_by_product(db, product_id)

    if not stats:
        raise not_found_exception(f"No reviews found for product '{product_id}'")

    return SentimentStatsResponse(product_id=product_id, **stats)
