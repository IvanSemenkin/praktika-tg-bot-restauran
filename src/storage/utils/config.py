from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

load_dotenv(ENV_PATH)

def get_groq_key() -> str:
    return os.getenv("GROQ_API_KEY")

def get_token() -> str:
    return os.getenv("TOKEN")

def get_log_level() -> str:
    return os.getenv("LOG_LEVEL")

def get_redis_host() -> str:
    return os.getenv("REDIS_HOST")

def get_redis_port() -> int:
    return int(os.getenv("REDIS_PORT"))

def get_redis_db() -> int:
    return int(os.getenv("REDIS_DB"))