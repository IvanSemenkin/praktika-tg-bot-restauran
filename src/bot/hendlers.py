from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import AI
from src.storage.utils.logger import logger
import redis
import os
from ai import ai_qwen_langchain


router = Router()
r = redis.Redis(host="localhost", port="6380", db=0)
user_id = r.incr("user_id_counter")


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.id}", reply_markup=kb.main)


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Это help")


@router.message(F.text.lower() == "ии")
async def ai_start(message: Message, state: FSMContext):
    await state.set_state(AI.ask)
    await message.answer(
        'Что бы вы хотели спросить? ИИ ответит только на вопросы по еде. Для завершения напишите "Пока", "Хватит", "Стоп"'
    )


@router.message(AI.ask)
async def ai_ask(message: Message, state: FSMContext):
    if (
        message.text.lower() == "хватит"
        or message.text.lower() == "пока"
        or message.text.lower() == "стоп"
    ):
        await message.answer("Пока")
        state.clear()
        return


    ans = ai_qwen_langchain(message.text)
    
    r.hset(f"chat_history:{message.from_user.id}", mapping={"user":message.text})
    logger.info('Redis user')
    r.hset(f"chat_history:{message.from_user.id}", mapping={"assistant":ans})
    logger.info('Redis assistant')
    await message.answer(ans)
