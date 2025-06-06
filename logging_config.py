# logging_config.py

import logging.config
import os

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/app.log",
                "when": "midnight",            # rotate daily
                "backupCount": 0,              # doesn't delete old files (we have setup scheduler for that)
                "encoding": "utf-8",
                "formatter": "default",
            },
        },
        "loggers": {
            "myapp.access": {
                "level": "DEBUG",
                "handlers": ["file"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
