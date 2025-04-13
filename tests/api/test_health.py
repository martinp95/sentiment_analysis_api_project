"""Test for the health check endpoint with real HTTP server and proper sync."""

from multiprocessing import Process

import pytest
from httpx import AsyncClient

from tests.utils import get_open_port, run_server, wait_for_port


@pytest.mark.asyncio
async def test_health_check():
    port = get_open_port()
    proc = Process(target=run_server, args=(port,))
    proc.start()

    try:
        await wait_for_port(port)

        async with AsyncClient(base_url=f"http://127.0.0.1:{port}") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}

    finally:
        proc.terminate()
        proc.join()
