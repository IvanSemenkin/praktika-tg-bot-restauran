from aiogram import Bot, Dispatcher
from src.bot.handlers import router 
from src.utils.logger import logger
import asyncio
from dotenv import load_dotenv
from aiogram.fsm.storage.redis import RedisStorage
from src.utils.config import Settings, ENV_PATH

load_dotenv(dotenv_path=ENV_PATH)

settings = Settings()

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
