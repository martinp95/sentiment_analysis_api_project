"""Pydantic model for sentiment statistics response."""

from pydantic import BaseModel, Field


class SentimentStatsResponse(BaseModel):
    """
    Output model representing sentiment statistics for a given product.

    Attributes:
        product_id (str): Identifier of the product.
        positive (float): Percentage of positive reviews.
        neutral (float): Percentage of neutral reviews.
        negative (float): Percentage of negative reviews.
    """

    product_id: str = Field(
        ...,
        example="SKU-98765",
        description="Product ID for which sentiment stats are calculated.",
    )
    positive: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        example=0.75,
        description="Percentage of reviews classified as positive.",
    )
    neutral: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        example=0.15,
        description="Percentage of reviews classified as neutral.",
    )
    negative: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        example=0.10,
        description="Percentage of reviews classified as negative.",
    )
