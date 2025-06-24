from aiogram import *
from aiogram.filters import *
from aiogram.types import *
from app.hendlers import router

import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
