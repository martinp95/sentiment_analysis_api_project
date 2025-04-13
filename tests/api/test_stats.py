"""End-to-end test for sentiment stats endpoint."""

from multiprocessing import Process
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.core.context import context
from tests.utils import AsyncCursorMock, get_open_port, run_server, wait_for_port


@pytest.mark.asyncio
async def test_stats_endpoint():
    """Test the /reviews/stats/{product_id} endpoint end-to-end."""
    port = get_open_port()

    # Setup mock data
    mock_reviews = [
        {"product_id": "prod1", "sentiment": "positive"},
        {"product_id": "prod1", "sentiment": "neutral"},
        {"product_id": "prod1", "sentiment": "positive"},
        {"product_id": "prod1", "sentiment": "negative"},
    ]

    mock_collection = AsyncMock()
    mock_collection.find = lambda *args, **kwargs: AsyncCursorMock(mock_reviews)

    mock_db = AsyncMock()
    mock_db.reviews = mock_collection

    with patch.object(context, "get_db", return_value=mock_db):
        proc = Process(target=run_server, args=(port,))
        proc.start()

        try:
            await wait_for_port(port)

            async with AsyncClient(base_url=f"http://127.0.0.1:{port}") as client:
                headers = {"X-API-Key": settings.api_key}
                response = await client.get("/reviews/stats/prod1", headers=headers)

                assert response.status_code == 200
                assert response.json() == {
                    "positive": 0.5,
                    "neutral": 0.25,
                    "negative": 0.25,
                    "product_id": "prod1",
                }

        finally:
            proc.terminate()
            proc.join()


@pytest.mark.asyncio
async def test_stats_endpoint_missing_token():
    """Should return 401 if no API key is provided."""
    port = get_open_port()
    proc = Process(target=run_server, args=(port,))
    proc.start()

    try:
        await wait_for_port(port)

        async with AsyncClient(base_url=f"http://127.0.0.1:{port}") as client:
            response = await client.get("/reviews/stats/prod1")  # No headers
            assert response.status_code == 401
            assert response.json()["detail"] == "Invalid or missing API key."

    finally:
        proc.terminate()
        proc.join()


@pytest.mark.asyncio
async def test_stats_endpoint_product_not_found():
    """Should return 404 if product ID has no reviews."""
    port = get_open_port()

    mock_collection = AsyncMock()
    mock_collection.find = lambda *args, **kwargs: AsyncCursorMock([])

    mock_db = AsyncMock()
    mock_db.reviews = mock_collection

    with patch.object(context, "get_db", return_value=mock_db):
        proc = Process(target=run_server, args=(port,))
        proc.start()

        try:
            await wait_for_port(port)

            async with AsyncClient(base_url=f"http://127.0.0.1:{port}") as client:
                headers = {"X-API-Key": settings.api_key}
                response = await client.get("/reviews/stats/prod1", headers=headers)

                assert response.status_code == 404
                assert "No reviews found" in response.json()["detail"]

        finally:
            proc.terminate()
            proc.join()
