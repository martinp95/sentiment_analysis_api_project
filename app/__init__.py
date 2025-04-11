"""Application factory with startup/shutdown lifecycle for the FastAPI project."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import health, sentiment, stats
from app.core.config import settings
from app.core.context import context
from app.core.security import API_KEY_NAME
from app.db.mongo import get_mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application context at startup."""
    client: AsyncIOMotorClient = get_mongo_client()
    db = client[settings.db_name]

    context.db = db  # App-wide DB inject into services

    yield

    client.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Sentiment Analysis API",
        version="1.0.0",
        description=(
            "This API allows users to analyze the sentiment of product reviews "
            "and track sentiment statistics perproduct in real time. "
            "Built with FastAPI and MongoDB. Fully containerized with Docker, CI/CD-ready, and extensible."
        ),
        contact={"name": "Martin Pelaez Diaz", "url": "https://github.com/martinp95"},
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

    # OpenAPI customization
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
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
