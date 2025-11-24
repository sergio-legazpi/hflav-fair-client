"""
Logger configuration for hflav_zenodo package.

This module provides a centralized logging configuration that can be imported
and used throughout the package.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger (typically __name__ of the calling module)
        level: Logging level (if None, defaults to INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if the logger hasn't been configured yet
    if not logger.handlers:
        # Set default level
        if level is None:
            level = logging.INFO

        logger.setLevel(level)

        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

        # Prevent propagation to root logger
        logger.propagate = False

    return logger


def set_log_level(logger: logging.Logger, level: int) -> None:
    """
    Set the logging level for a logger and all its handlers.

    Args:
        logger: Logger instance to configure
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
