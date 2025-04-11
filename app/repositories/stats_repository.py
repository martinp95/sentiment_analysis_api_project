"""Repository for sentiment statistics from MongoDB."""

from collections import Counter
from typing import Dict

from motor.motor_asyncio import AsyncIOMotorDatabase


async def fetch_sentiment_distribution_by_product(
    db: AsyncIOMotorDatabase, product_id: str
) -> Dict[str, float]:
    """
    Aggregate sentiment statistics for a specific product.

    Args:
        db (AsyncIOMotorDatabase): MongoDB database instance.
        product_id (str): Product ID to filter reviews.

    Returns:
        Dict[str, float]: Sentiment distribution for the product.
    """
    cursor = db.reviews.find({"product_id": product_id}, {"sentiment": 1})
    sentiments = [doc async for doc in cursor]
    total = len(sentiments)

    if total == 0:
        return {}

    counter = Counter(doc["sentiment"] for doc in sentiments)

    return {
        "positive": round(counter.get("positive", 0) / total, 2),
        "neutral": round(counter.get("neutral", 0) / total, 2),
        "negative": round(counter.get("negative", 0) / total, 2),
    }
