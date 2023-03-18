from typing import Union

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message

from core import crud


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.chat.id == crud.get_bot_by_token(bot.token).manager_id

