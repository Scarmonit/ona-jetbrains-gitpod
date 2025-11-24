"""Structured logging configuration for the application.

This module provides a standardized logging setup with structured output
including timestamps, log levels, module names, and messages.
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure structured logging for the application.

    Sets up the root logger with a consistent format including timestamp,
    log level, module name, and message. Uses stdout as the output stream.

    Args:
        level: Logging level as a string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to INFO.

    Returns:
        logging.Logger: The configured root logger instance.

    Example:
        >>> logger = setup_logging("DEBUG")
        >>> logger.info("Application started")
        2024-01-15 10:30:00 - INFO - logging_config - Application started
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Define log format with structured output
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance for the specified module.

    Args:
        name: The name for the logger, typically __name__ of the calling module.
              If None, returns the root logger.

    Returns:
        logging.Logger: A logger instance for the specified module.
    """
    return logging.getLogger(name)
