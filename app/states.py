from aiogram.fsm.state import *
from aiogram.fsm.context import *


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()