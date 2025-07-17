import logging
from src.utils.config import Settings

LOG_LEVEL = "INFO"

settings = Settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("food-bot")
