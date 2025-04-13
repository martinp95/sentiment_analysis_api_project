"""Test for the health check endpoint with real HTTP server and proper sync."""

import asyncio
import socket
from multiprocessing import Process

import pytest
import uvicorn
from httpx import AsyncClient


def get_open_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def run_server(port: int):
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
    )


async def wait_for_port(port: int, host: str = "127.0.0.1", timeout: float = 10.0):
    """Wait until a port starts accepting TCP connections."""
    start = asyncio.get_event_loop().time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            await asyncio.sleep(0.1)
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError(
                    f"Timed out waiting for {host}:{port} to be available"
                )


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
