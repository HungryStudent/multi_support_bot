from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задать вопрос")
        ],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отмена")]], resize_keyboard=True)
