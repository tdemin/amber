import logging

from project_amber.config import config

level = logging.INFO
if config["loglevel"] == 0: level = logging.ERROR
if config["loglevel"] == 1: level = logging.WARN

logging.basicConfig(level=level)
logger = logging.getLogger("amber_backend")


def log(message):
    """
    Wrapper for the logger calls. Only intended to be used in DB code.
    Corresponds to loglevel 2.
    """
    logger.info(message)


def warn(message):
    """
    Wrapper for the logger calls. Corresponds to loglevel 1.
    """
    logger.warning(message)


def error(message):
    """
    Wrapper for the error messages. Loglevel 0.
    """
    logger.error(message)
