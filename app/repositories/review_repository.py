"""Repository for storing and retrieving review data from MongoDB."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.review import ReviewRequest, ReviewResponse


async def save_review(
    db: AsyncIOMotorDatabase,
    review: ReviewRequest,
    result: ReviewResponse,
) -> None:
    """
    Persist the review and sentiment result to the database.

    Args:
        db (AsyncIOMotorDatabase): The MongoDB database instance.
        review (ReviewRequest): The input review.
        result (ReviewResponse): The predicted sentiment and confidence.
    """
    await db.reviews.insert_one(
        {
            "product_id": review.product_id,
            "review": review.review,
            "sentiment": result.sentiment,
            "confidence": result.confidence,
        }
    )
