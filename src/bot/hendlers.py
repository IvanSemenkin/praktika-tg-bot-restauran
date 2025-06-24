from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import Register
from src.storage.utils.logger import logger
import redis
import os


router = Router()
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)
user_id = r.incr("user_id_counter")


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет", reply_markup=kb.main)


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Это help")


@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer("Каталог товаров:", reply_markup=kb.catalog)


@router.callback_query(F.data == "t-shirt")
async def t_shirt(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Вы купили майку")


@router.message(Command("reg"))
async def register(message: Message, state: FSMContext):
    logger.info("Началась регистрация")
    await state.set_state(Register.name)
    await message.answer("Введите ваше имя:")


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    r.set(f"user:{user_id}:name", message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст:")


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    r.set(f"user:{user_id}:age", message.text)
    await state.set_state(Register.number)
    await message.answer("Нажмите чтобы отправить ваш номер:", reply_markup=kb.number)


@router.message(Register.number)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    r.set(f"user:{user_id}:number", message.contact.phone_number)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        f"Спасибо, регистрация завершена!\n"
        f"Привет, {data['name']}, тебе {data['age']} лет, и вот твой номер телефона: {data['number']}"
    )

    a = []
    for i in range(1, user_id + 1):
        a.append((f"user:{i} name", (r.get(f"user:{i}:name") or b"").decode()))
        a.append((f"user:{i} age", (r.get(f"user:{i}:age") or b"").decode()))
        a.append((f"user:{i} number", (r.get(f"user:{i}:number") or b"").decode()))

    lines = []
    for key, value in a:
        lines.append(f"{key}: {value}")
    text = "\n".join(lines)
    await message.answer(text)
