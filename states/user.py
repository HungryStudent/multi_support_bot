from aiogram.fsm.state import StatesGroup, State


class CreateBot(StatesGroup):
    name = State()
    api_token = State()


class ChangeHelloMsg(StatesGroup):
    text = State()
