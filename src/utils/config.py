from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    def __init__(self):
        self.groq_api_key: str = os.getenv("GROQ_API_KEY")
        self.token: str = os.getenv("TOKEN")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.redis_host: str = os.getenv("REDIS_HOST")
        self.redis_port: int = int(os.getenv("REDIS_PORT", 6379))
        self.redis_db: int = int(os.getenv("REDIS_DB", 0))
