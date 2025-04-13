"""Utility helpers for end-to-end API testing."""

import asyncio
import socket

import uvicorn


def get_open_port() -> int:
    """
    Get an available random port from the OS.

    Returns:
        int: A free port number on localhost.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def run_server(port: int):
    """
    Start the FastAPI application with Uvicorn on the specified port.

    Args:
        port (int): The port number to use.
    """
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
    )


async def wait_for_port(port: int, host: str = "127.0.0.1", timeout: float = 20.0):
    """
    Wait until the given port is accepting TCP connections.

    Args:
        port (int): Port to wait for.
        host (str): Host address to check.
        timeout (float): Max time to wait before raising TimeoutError.
    """
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


class AsyncCursorMock:
    """
    A simple async iterable to mock MongoDB cursors.

    Attributes:
        _data (list): List of documents to yield asynchronously.
    """

    def __init__(self, data):
        self._data = data

    def __aiter__(self):
        return self._async_iterator()

    async def _async_iterator(self):
        for item in self._data:
            yield item
