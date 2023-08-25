from aiogram import F
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from core import crud
from filters.is_admin import IsAdminFilter

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

    if message.photo:
        await bot.send_photo(int(hashtag[3:]), message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        await bot.send_video(int(hashtag[3:]), message.video.file_id, caption=message.caption)
    elif message.document:
        await bot.send_document(int(hashtag[3:]), message.document.file_id, caption=message.caption)
    else:
        await bot.send_message(int(hashtag[3:]), message.text)
