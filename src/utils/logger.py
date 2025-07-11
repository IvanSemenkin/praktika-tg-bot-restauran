import logging
import os
from src.utils.config import get_log_level

LOG_LEVEL = "INFO"

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("food-bot")
