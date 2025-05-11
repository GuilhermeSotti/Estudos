import logging
import sys
from config.settings import LOG_LEVEL, LOG_FORMAT

def setup_logging():
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        stream=sys.stdout
    )
