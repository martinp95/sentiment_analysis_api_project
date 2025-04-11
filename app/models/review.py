"""Pydantic models for review requests and responses."""

from typing import Literal

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    """
    Input model for submitting a product review to analyze sentiment.

    Attributes:
        product_id (str): Unique identifier of the product being reviewed.
        review (str): Text content of the review.
    """

    product_id: str = Field(
        ...,
        example="SKU-98765",
        description="Unique identifier for the product being reviewed.",
    )
    review: str = Field(
        ...,
        example="Absolutely loved the build quality and performance!",
        description="The full text of the user review.",
    )


class ReviewResponse(BaseModel):
    """
    Output model representing the result of sentiment analysis.

    Attributes:
        sentiment (str): Predicted sentiment label.
        confidence (float): Confidence score (0.0 - 1.0).
    """

    sentiment: Literal["positive", "neutral", "negative"] = Field(
        ..., description="Predicted sentiment class for the given review."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        example=0.92,
        description="Confidence score for the predicted sentiment label.",
    )
