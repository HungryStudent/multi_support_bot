from aiogram import Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated
from aiogram import F

from core import crud

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=(KICKED | IS_NOT_MEMBER) >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    bot_data = crud.get_bot_by_token(bot.token)
    if bot_data.owner_id != event.from_user.id:
        await bot.leave_chat(event.chat.id)
        return
    await bot.send_message(event.chat.id, "Выдайте мне права админстратора")


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(KICKED | MEMBER | IS_NOT_MEMBER) >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot: Bot):
    bot_data = crud.get_bot_by_token(bot.token)
    if bot_data.owner_id != event.from_user.id:
        await bot.leave_chat(event.chat.id)
        return
    await bot.send_message(event.chat.id, "Права выданы!")
    crud.set_bot_manager_id(bot.token, event.chat.id)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(MEMBER | ADMINISTRATOR) >> (IS_NOT_MEMBER | KICKED)))
async def bot_delete_from_group(event: ChatMemberUpdated, bot: Bot):
    crud.set_bot_manager_id(bot.token, None)
