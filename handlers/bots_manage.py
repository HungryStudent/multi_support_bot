import datetime

from aiogram import Router, Bot, Dispatcher
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, \
    KICKED
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ChatMemberUpdated
from aiogram import F
from aiogram.utils.token import TokenValidationError

from keyboards import user as user_kb
from config import ADMINS, OTHER_BOTS_URL
from core import crud, schemas
from states.user import CreateBot, ChangeHelloMsg

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Text("Мои проекты"))
async def show_bots(message: Message):
    await message.answer("Список ботов:", reply_markup=user_kb.get_bots(crud.get_bots_by_user_id(message.from_user.id)))


@router.callback_query(user_kb.BotFactory.filter())
async def show_bot(call: CallbackQuery, callback_data: user_kb.BotFactory):
    bot = crud.get_bot(callback_data.bot_id)
    await call.message.answer(f"{bot.name}", reply_markup=user_kb.get_bot(bot.bot_id))
    await call.answer()


@router.callback_query(user_kb.MenuBotFactory.filter(F.action == 'change_hello_msg'))
async def change_hello_msg(call: CallbackQuery, callback_data: user_kb.MenuBotFactory, state: FSMContext):
    await call.message.answer("Введите приветственное сообщение", reply_markup=user_kb.cancel)
    await state.set_state(ChangeHelloMsg.text)
    await state.update_data(bot_id=callback_data.bot_id)
    await call.answer()


@router.message(ChangeHelloMsg.text)
async def change_hello_msg_finish(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Приветствие изменено')
    data = await state.get_data()
    await state.clear()
    crud.change_hello_msg(message.text, data['bot_id'])


@router.callback_query(user_kb.MenuBotFactory.filter(F.action == "delete"))
async def start_delete_bot(call: CallbackQuery, callback_data: user_kb.MenuBotFactory):
    await call.message.edit_text("Вы действительно хотите удалить проект?",
                                 reply_markup=user_kb.get_delete(callback_data.bot_id))


@router.callback_query(user_kb.MenuBotFactory.filter(F.action.in_(["sure_delete", "cancel_delete"])))
async def delete_bot(call: CallbackQuery, callback_data: user_kb.MenuBotFactory, bot: Bot):
    dop_bot = crud.get_bot(callback_data.bot_id)
    if callback_data.action == "sure_delete":
        crud.delete_bot(callback_data.bot_id)
        await call.message.edit_text("Проект удален",
                                     reply_markup=user_kb.get_bots(crud.get_bots_by_user_id(call.from_user.id)))
        deleted_bot = Bot(token=dop_bot.api_token, session=bot.session)
        try:
            await deleted_bot.get_me()
        except TelegramUnauthorizedError:
            return
        await deleted_bot.delete_webhook(drop_pending_updates=True)
    elif callback_data.action == "cancel_delete":
        await call.message.edit_text(f"{dop_bot.name}", reply_markup=user_kb.get_bot(dop_bot.bot_id))


@router.message(Text("Добавить проект"))
async def start_add_bot_by_msg(message: Message, state: FSMContext):
    await message.answer("Как назовём бота?", reply_markup=user_kb.cancel)
    await state.set_state(CreateBot.name)


@router.callback_query(Text("add_bot"))
async def start_add_bot(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Как назовём бота?", reply_markup=user_kb.cancel)
    await state.set_state(CreateBot.name)
    await call.answer()


@router.message(CreateBot.name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("""Отличное название!

Пришли токен бота ⤵️""")
    await state.set_state(CreateBot.api_token)


@router.message(CreateBot.api_token)
async def enter_api_token(message: Message, state: FSMContext):
    new_bot = Bot(message.text)
    try:
        await new_bot.get_me()
    except (TokenValidationError, TelegramUnauthorizedError):
        await message.answer("Введён неверный токен, повторите попытку")
        return
    if crud.get_bot_by_token(message.text):
        await message.answer("Бот с таким токеном уже существует")
        return
    await state.update_data(api_token=message.text)

    bot_data = await state.get_data()
    bot_data["owner_id"] = message.from_user.id
    bot_data['hello_msg'] = 'Здравствуйте! Операторы онлайн, расскажите что у вас случилось?'
    crud.add_bot(schemas.BotCreate(**bot_data))
    my_bot = Bot(message.text)
    bot_info = await my_bot.get_me()
    await message.answer(f"""Проект создан💪🏻 

Добавьте бота @{bot_info.username} в группу для модераторов, выдав права администратора.""",
                         reply_markup=user_kb.menu)
    await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=new_bot.token))
    await state.clear()
