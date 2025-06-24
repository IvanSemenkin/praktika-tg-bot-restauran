from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

class AI(StatesGroup):
    ask = State()