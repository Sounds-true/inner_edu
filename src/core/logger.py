"""Structured logging configuration using structlog."""

import sys
import structlog
from typing import Any, Dict
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_dir: Path = Path("data/logs")) -> None:
    """Configure structured logging."""

    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                ]
            ),
            structlog.processors.dict_tracebacks,
            structlog.dev.ConsoleRenderer() if log_level == "DEBUG" else structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str, **context: Any) -> structlog.BoundLogger:
    """Get a logger instance with optional context."""
    logger = structlog.get_logger(name)
    if context:
        logger = logger.bind(**context)
    return logger


def log_child_interaction(
    logger: structlog.BoundLogger,
    user_id: str,
    message_type: str,
    **kwargs: Any
) -> None:
    """
    Log child interaction with strict PII protection.

    For children, we're extra careful about:
    - Full name protection
    - Age information
    - Location data
    - Any identifying information
    """
    # Remove any potential PII from kwargs
    safe_kwargs = {
        k: v for k, v in kwargs.items()
        if k not in ["child_name", "full_name", "age", "school", "address", "parent_name"]
    }

    logger.info(
        "child_interaction",
        user_id=user_id,
        message_type=message_type,
        **safe_kwargs
    )


def log_parent_notification(
    logger: structlog.BoundLogger,
    event_type: str,
    severity: str,
    user_id: str,
    parent_id: str,
    **details: Any
) -> None:
    """Log parent notifications (for screening, alerts, reports)."""
    logger.info(
        "parent_notification",
        event_type=event_type,
        severity=severity,
        user_id=user_id,
        parent_id=parent_id,
        **details
    )


def log_screening_event(
    logger: structlog.BoundLogger,
    event_type: str,
    concern_level: str,
    user_id: str,
    **metrics: Any
) -> None:
    """Log screening events for therapeutic transition detection."""
    logger.warning(
        "screening_event",
        event_type=event_type,
        concern_level=concern_level,
        user_id=user_id,
        **metrics
    )
