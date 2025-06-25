from aiogram.fsm.state import State, StatesGroup


class AI(StatesGroup):
    ask = State()