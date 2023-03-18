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


@router.message(F.reply_to_message)
async def answer_to_ques(message: Message, bot: Bot):
    entities = message.reply_to_message.entities
    hashtag = entities[-1].extract_from(message.reply_to_message.text)
    await bot.send_message(int(hashtag[3:]), message.text)
