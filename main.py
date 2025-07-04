from aiogram import Bot, Dispatcher
from src.bot.handlers import router
from src.storage.utils.logger import logger

import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

logger.info("Бот запущен")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
