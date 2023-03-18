from typing import Any

from aiogram import Router
from aiogram.handlers import ErrorHandler
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ErrorEvent


router = Router()

#
# @router.errors()
# class MyHandler(ErrorHandler):
#     async def handle(self) -> Any:
#         print(self)