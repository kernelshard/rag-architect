import logging
import logging.config

import structlog

from .config import settings

DEFAULT_LOG_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.LOG_LEVEL,
        }
    },
    "root": {"handlers": ["console"], "level": settings.LOG_LEVEL},
}


def configure_logging() -> None:
    """
    Configure structured JSON logging.
    """
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    )

    # structlog processors chain
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # merges context vars (useful for trace_id later)
            structlog.processors.TimeStamper(fmt="iso"),  # adds ISO timestamp
            structlog.processors.add_log_level,  # adds "level"
            structlog.processors.StackInfoRenderer(),  # adds stack info if exc_info=True
            structlog.processors.format_exc_info,  # formats exceptions cleanly
            structlog.processors.JSONRenderer(),  # outputs structured JSON
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        ),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """
    Returns a structlog logger instance bound with module name and environment.
    """
    logger = structlog.get_logger(name)
    configure_logging()
    return logger.bind(module=name, environment=settings.ENV)
