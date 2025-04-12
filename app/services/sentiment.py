"""Business logic for sentiment analysis service."""

import torch
from torch.nn.functional import softmax

from app.core.context import context
from app.core.logger import logger
from app.models.review import ReviewRequest, ReviewResponse
from app.repositories.review_repository import save_review


async def analyze_and_store_sentiment(request: ReviewRequest) -> ReviewResponse:
    """
    Analyze the sentiment of a product review using a pre-trained transformer model
    and store the result in the database.

    Args:
        request (ReviewRequest): Review data including text and product ID.

    Returns:
        ReviewResponse: Sentiment label and confidence score.
    """
    logger.info(f"Starting sentiment analysis for product: {request.product_id}")

    # Get the model and tokenizer from context
    model, tokenizer = context.get_model()
    device = context.get_device()  # Get the device (CPU or GPU)
    model.to(device)  # Move the model to the appropriate device

    try:
        # Tokenize and encode the input review
        inputs = tokenizer(
            request.review,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )
        inputs = {key: val.to(device) for key, val in inputs.items()}

        logger.debug(f"Tokenized input: {inputs}")

        # Run the model inference
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = softmax(outputs.logits, dim=1).squeeze()

        # Determine sentiment label and confidence
        confidence, predicted_class = torch.max(probabilities, dim=0)
        sentiment_label = "neutral"
        if confidence >= 0.75:
            sentiment_label = "positive" if predicted_class == 1 else "negative"

        logger.info(
            f"Predicted sentiment: {sentiment_label} "
            f"(confidence={confidence.item():.2f}) for product={request.product_id}"
        )

        db = context.get_db()  # Get the MongoDB database instance

        response = ReviewResponse(
            sentiment=sentiment_label, confidence=round(confidence.item(), 2)
        )

        # Save the result in MongoDB
        await save_review(db, request, response)

        return response
    except Exception as e:
        logger.exception(f"Sentiment analysis failed due to unexpected error: {e}")
        raise
