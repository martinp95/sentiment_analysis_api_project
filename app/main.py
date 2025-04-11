"""Entry point for the FastAPI application."""

from app import create_app

# Create the FastAPI application instance using the factory pattern
app = create_app()
