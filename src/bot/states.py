from aiogram.fsm.state import State, StatesGroup


class AI(StatesGroup):
    ask = State()
    
class Clear_db(StatesGroup):
    wait_clear = State()
    
class GetInfoID(StatesGroup):
    id = State()
    type_info = State()

class DelInfoID(StatesGroup):
    id = State()
    wait_del = State()

class DelMyInfo(StatesGroup):
    wait_del = State()