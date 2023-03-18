from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import schemas

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить проект"),
            KeyboardButton(text="Мои проекты")
        ],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отмена")]],
                             resize_keyboard=True)


def get_bots(bots: List[schemas.BotOut]):
    builder = InlineKeyboardBuilder()
    for bot in bots:
        builder.add(InlineKeyboardButton(text=bot.name, callback_data=bot.bot_id))
    builder.add(InlineKeyboardButton(text="Добавить бота", callback_data="add_bot"))
    builder.adjust(1)
    return builder.as_markup()
