import datetime

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import F

from keyboards import admin as admin_kb
from keyboards import user as user_kb
# from keyboards import user as user_kb
from config import ADMINS, TOKEN
from core import crud, schemas
from states.admin import CreateBot

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    if not crud.get_user(message.from_user.id):
        crud.add_user(schemas.UserCreate(user_id=message.from_user.id, username=message.from_user.username,
                                         reg_time=datetime.datetime.now()))
    if message.from_user.id in ADMINS:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu
    await message.answer("""Привет! Я помогу тебе создать бота обратной связи🤖

Для начала нажми «Добавить проект»""", reply_markup=kb)


@router.message(Text("Отмена"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in ADMINS:
        kb = admin_kb.menu
    else:
        kb = user_kb.menu
    await message.answer("Ввод остановлен", reply_markup=kb)
