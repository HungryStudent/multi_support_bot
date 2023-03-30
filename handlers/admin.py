from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

from config import ADMINS
from core import crud

router = Router()
router.message.filter(F.from_user.id.in_(ADMINS))


@router.message(Command("stat"))
async def show_stat(message: Message):
    stat_data = crud.get_stat()
    await message.answer(f"Количество пользователей: {stat_data[0]}\nКоличество ботов: {stat_data[1]}")


