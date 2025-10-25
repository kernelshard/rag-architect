import logging

import logging.config

from typing import Dict

from .config import settings


DEFAULT_LOG_CONFIG: Dict = {
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


def configure_logging():
    logging.config.dictConfig(DEFAULT_LOG_CONFIG)


def get_logger(name: str):
    return logging.getLogger(name)
