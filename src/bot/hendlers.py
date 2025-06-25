from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import AI, Clear_db
from src.storage.utils.logger import logger
import redis
import os
from ai import ai_qwen_langchain


router = Router()
r = redis.Redis(host="localhost", port="6380", db=0)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.id}", reply_markup=kb.main)


@router.message(Command("info"))
async def help(message: Message):
    user = ''
    ai = ''
    for i in range(1, 11):
        try:
            user = user + f"{i}. {r.hget(f"chat_history:{message.from_user.id}:{i}", "user").decode()} \n\n"
            ai = ai + f"{i}. {r.hget(f"chat_history:{message.from_user.id}:{i}", "assistant").decode()} \n\n"
        except AttributeError:
            logger.info(f'help stop on {i}')
            break
    await message.answer(f"User: \n{user}")
    await message.answer(f"AI: \n{ai}")



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
        await state.clear()
        return


    ans = ai_qwen_langchain(message.text, message, r)
    
    us_count = r.incr(f"{message.from_user.id}_counter")
    
    
    if int(us_count) >= 10:
        r.set(f"{message.from_user.id}_counter", 0)
        logger.info('counter_clear')
    
    r.hset(f"chat_history:{message.from_user.id}:{us_count}", mapping={"user":message.text, "assistant":ans})
    
    await message.answer(ans)

@router.message(Command("cls"))
async def help(message: Message, state: FSMContext):
    await state.set_state(Clear_db.wait_clear)
    await message.answer('Вы уверены? (Да/Нет)')
    

@router.message(Clear_db.wait_clear)
async def clear_w(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        r.flushdb()
        await state.clear()
        await message.answer('БД успешно очишена')
    elif message.text.lower() == 'нет':
        await message.answer('Очистка отменена')
        state.clear()
        