"""Business logic for sentiment analysis service."""

import random

from app.core.context import context
from app.models.review import ReviewRequest, ReviewResponse
from app.repositories.review_repository import save_review


async def analyze_and_store_sentiment(request: ReviewRequest) -> ReviewResponse:
    """
    Perform sentiment analysis and persist the result in MongoDB.

    Args:
        request (ReviewRequest): Incoming review.

    Returns:
        ReviewResponse: Sentiment result.
    """
    db = context.get_db()  # Get the MongoDB database instance

    # Simulated prediction logic (to be replaced later)
    sentiment = random.choice(["positive", "neutral", "negative"])
    confidence = round(random.uniform(0.7, 0.99), 2)

    response = ReviewResponse(sentiment=sentiment, confidence=confidence)

    # Save the result in MongoDB
    await save_review(db, request, response)

    return response
