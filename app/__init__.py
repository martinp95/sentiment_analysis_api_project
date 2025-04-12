"""Application factory with startup/shutdown lifecycle for the FastAPI project."""

from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from motor.motor_asyncio import AsyncIOMotorClient
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.api import health, sentiment, stats
from app.core.config import settings
from app.core.context import context
from app.core.security import API_KEY_NAME
from app.db.mongo import get_mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan handler.

    This function is called on startup and shutdown of the app.

    - Initializes MongoDB connection and stores it in the global context.
    - Loads a pre-trained sentiment analysis model from HuggingFace Transformers.
    - Sets device to CUDA (GPU) if available, otherwise CPU.
    """
    # BD set up
    client: AsyncIOMotorClient = get_mongo_client()
    db = client[settings.db_name]
    context.db = db

    # Load ML model
    tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(settings.model_name)
    model.eval()

    # Inject into global context
    context.tokenizer = tokenizer
    context.model = model
    context.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    yield

    client.close()


def create_app() -> FastAPI:
    """
    Application factory that sets up the FastAPI instance.

    Includes route registration, OpenAPI customization, and lifecycle management.
    """
    app = FastAPI(
        title="Sentiment Analysis API",
        version="1.0.0",
        description=(
            "This API allows users to analyze the sentiment of product reviews "
            "and track sentiment statistics per product in real time.\n\n"
            "Built with **FastAPI** and **MongoDB**. Fully containerized with Docker, "
            "CI/CD-ready, and extensible with pluggable ML models."
        ),
        contact={
            "name": "Martin Pelaez Diaz",
            "url": "https://github.com/martinp95",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        lifespan=lifespan,
    )

    # Register API routers
    app.include_router(health.router)
    app.include_router(sentiment.router)
    app.include_router(stats.router)

    # Customize OpenAPI to support API Key header
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            contact=app.contact,
            license_info=app.license_info,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "APIKeyHeader": {
                "type": "apiKey",
                "in": "header",
                "name": API_KEY_NAME,
            }
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", [{"APIKeyHeader": []}])

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app
