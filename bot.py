import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.utils.markdown import html_decoration as fmt
from aiogram.utils.token import TokenValidationError

import core
from config import TOKEN, ADMINS
from core import crud, models, schemas
from core.database import engine
from handlers import bots_manage, user, other, dop, admin
from polling_manager import PollingManager

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="add_bot",
            description="add bot, usage '/add_bot 123456789:qwertyuiopasdfgh'",
        ),
        BotCommand(
            command="stop_bot",
            description="stop bot, usage '/stop_bot 123456789'",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def on_bot_startup(bot: Bot):
    await set_commands(bot)


async def on_bot_shutdown(bot: Bot):
    pass


async def on_startup(dp_for_new_bot, polling_manager):
    bots = crud.get_bots()
    for bot in bots:
        await core.manage_bots.add_bot(bot.api_token, dp_for_new_bot, polling_manager)


async def on_shutdown(bots: List[Bot]):
    for bot in bots:
        await on_bot_shutdown(bot)


async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    models.Base.metadata.create_all(bind=engine)
    TOKENS = [TOKEN]
    bots = [Bot(token) for token in TOKENS]

    dp = Dispatcher(events_isolation=SimpleEventIsolation())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(user.router, bots_manage.router, other.router, admin.router)

    dop_dp = Dispatcher(events_isolation=SimpleEventIsolation())
    dop_dp.include_routers(dop.user.router, dop.system.router, dop.admin.router)

    polling_manager = PollingManager()

    for bot in bots:
        await bot.get_updates(offset=-1)
    await dp.start_polling(*bots, dp_for_new_bot=dop_dp, polling_manager=polling_manager)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit")
