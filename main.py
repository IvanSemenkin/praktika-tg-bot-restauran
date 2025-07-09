from aiogram import Bot, Dispatcher
from src.bot.handlers import router
import redis    
from src.storage.utils.logger import logger
import subprocess
import asyncio
from dotenv import load_dotenv
from time import sleep
from aiogram.fsm.storage.redis import RedisStorage
import os

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
storage = RedisStorage.from_url('redis://localhost:6380/0')
dp = Dispatcher(storage=storage)

logger.info("Бот запущен")

# try:
#     r = redis.Redis(host="localhost", port="6380", db=0)
#     r.ping()
#     logger.info("Redis уже запущен")
# except redis.ConnectionError:
#     try:
#         subprocess.run(["sudo", "systemctl", "start", "redis-server"], check=True)
#         sleep(1)
#     except subprocess.CalledProcessError:
#         logger.info("Не удалось запустить Redis через systemd")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
