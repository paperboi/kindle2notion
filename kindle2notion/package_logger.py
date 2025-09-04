import logging
from rich.logging import RichHandler

LOG_LEVEL = "INFO"
logger = logging.getLogger("kindle2notion")
logger.setLevel(LOG_LEVEL)

handler = RichHandler(show_time=False, rich_tracebacks=True, markup=True)
logger.addHandler(handler)
