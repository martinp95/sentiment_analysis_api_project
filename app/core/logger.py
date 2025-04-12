"""Logging configuration using loguru."""

import sys

from loguru import logger
from loguru._logger import Logger


def configure_logger(level: str = "DEBUG") -> Logger:
    """
    Configure the global logger.

    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        logger (loguru.Logger): Configured logger instance.
    """
    # Remove default logger to avoid duplicate logs
    logger.remove()

    # Add a new logger with the specified level and format
    logger.add(
        sys.stdout,
        level=level.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        backtrace=True,
        diagnose=True,
    )

    return logger
