from aiogram.fsm.state import State, StatesGroup


class AI(StatesGroup):
    ask = State()
    
class Clear_db(StatesGroup):
    wait_clear = State()