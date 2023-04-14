from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from core import schemas


class BotFactory(CallbackData, prefix="bot"):
    bot_id: int


class MenuBotFactory(CallbackData, prefix="menu_bot"):
    action: str
    bot_id: int


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
        builder.button(text=f"{bot.name} ({bot.ques_count})", callback_data=BotFactory(bot_id=bot.bot_id))
    builder.add(InlineKeyboardButton(text="Добавить бота", callback_data="add_bot"))
    builder.adjust(1)
    return builder.as_markup()


def get_bot(bot_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить приветствие", callback_data=MenuBotFactory(action="change_hello_msg", bot_id=bot_id))
    builder.button(text="Удалить проект", callback_data=MenuBotFactory(action="delete", bot_id=bot_id))
    return builder.as_markup()


def get_delete(bot_id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=MenuBotFactory(action="sure_delete", bot_id=bot_id))
    builder.button(text="Нет", callback_data=MenuBotFactory(action="cancel_delete", bot_id=bot_id))
    return builder.as_markup()
