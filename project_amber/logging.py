import logging

from project_amber.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sjbackend")

def log(message):
    """
    Wrapper for the logger calls. Only intended to be used in DB code.
    """
    # This wrapper only logs things in case of loglevel being set to 2
    # (log requests).
    if config["loglevel"] == 2:
        logger.info(message)

def logError(message):
    """
    Wrapper for the error messages.
    """
    logger.error(message)
