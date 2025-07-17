from aiogram import Bot, Dispatcher
from src.bot.handlers import router 
from src.utils.logger import logger
import asyncio
from aiogram.fsm.storage.redis import RedisStorage
from src.utils.config import Settings

settings = Settings()

logger.info(f"token: {settings.token}")
logger.info(f"redis_db: {settings.redis_db}")
logger.info(f"redis_host: {settings.redis_host}")
logger.info(f"redis_port: {settings.redis_port}")
logger.info(f"groq_api_key: {settings.groq_api_key}")
logger.info(f"log_level: {settings.log_level}")

bot = Bot(token=settings.token)

storage = RedisStorage.from_url(f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}')
dp = Dispatcher(storage=storage)

logger.info("Бот запущен")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
