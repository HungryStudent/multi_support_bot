from aiogram.fsm.state import StatesGroup, State


class AskQues(StatesGroup):
    text = State()
