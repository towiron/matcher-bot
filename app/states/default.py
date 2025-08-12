from aiogram.fsm.state import State, StatesGroup


class LikeResponse(StatesGroup):
    response = State()

class Search(StatesGroup):
    search = State()
    message = State()
