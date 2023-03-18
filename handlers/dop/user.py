import datetime

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import F

from filters.chat_type import ChatTypeFilter
from keyboards import admin as admin_kb
from keyboards.dop import user as user_kb
from config import ADMINS, TOKEN
from core import crud, schemas
from states.dop.user import AskQues

router = Router()
router.message.filter(ChatTypeFilter(chat_type="private"))


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Здравствуйте")


@router.message(Text("Отмена"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ввод остановлен", reply_markup=user_kb.cancel)


@router.message(F.text)
async def send_ques(message: Message, bot: Bot):
    my_bot = crud.get_bot_by_token(bot.token)
    ques = schemas.QuestionCreate(bot_id=my_bot.bot_id, user_id=message.from_user.id, msg_id=message.message_id,
                                  ques=message.text,
                                  create_time=datetime.datetime.now())
    manager_id = crud.add_ques(ques)[0]
    if manager_id:
        await bot.send_message(manager_id, message.text + f"\n\n#id{message.from_user.id}")
