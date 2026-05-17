"""Structured logging configuration for SAGA using structlog.

Sets up structlog with JSON output in production and human-readable output in development,
keyed on the SAGA_LOG_FORMAT environment variable ('json' or 'console', default 'console').
"""

from __future__ import annotations

import logging
import os

import structlog


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structlog for SAGA.

    Args:
        log_level: Logging level string (default 'INFO').
    """
    log_format = os.getenv("SAGA_LOG_FORMAT", "console")
    level = getattr(logging, log_level.upper(), logging.INFO)

    if log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
