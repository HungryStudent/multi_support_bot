import datetime

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import F

from filters.is_admin import IsAdminFilter
from keyboards import admin as admin_kb
from keyboards.dop import user as user_kb
from config import ADMINS, TOKEN
from core import crud, schemas
from states.dop.user import AskQues

router = Router()
router.message.filter(IsAdminFilter())


@router.message(Command("ban"))
async def ban_user(message: Message, bot: Bot):
    user_id = message.text.split(" ")[1]
    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer("Введите корректный user_id")
        return
    crud.ban_user(bot.id, user_id)
    await message.answer("Пользователь забанен")


@router.message(Command("unban"))
async def unban_user(message: Message, bot: Bot):
    user_id = message.text.split(" ")[1]
    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer("Введите корректный user_id")
        return
    crud.unban_user(bot.id, user_id)
    await message.answer("Пользователь разбанен")


@router.message(F.reply_to_message)
async def answer_to_ques(message: Message, bot: Bot):
    entities = message.reply_to_message.entities
    try:
        hashtag = entities[-1].extract_from(message.reply_to_message.text)
    except TypeError:
        try:
            if message.reply_to_message.caption.split("\n")[2] != "":
                hashtag_start = message.reply_to_message.caption.find("#id")
                hashtag_end = message.reply_to_message.caption.find("\n", hashtag_start) + 1
                hashtag = message.reply_to_message.caption[hashtag_start:hashtag_end]
        except IndexError:
            hashtag = message.reply_to_message.caption
    await bot.send_message(int(hashtag[3:]), message.text)
