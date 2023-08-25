import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)
from aiohttp import web

from config import MAIN_BOT_TOKEN, OTHER_BOTS_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT, MAIN_BOT_PATH, \
    BASE_URL, OTHER_BOTS_URL
from core import crud, models
from core.database import engine
from handlers import bots_manage, user, other, dop, admin

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


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(f"{BASE_URL}{MAIN_BOT_PATH}")
    bots = crud.get_bots()
    for db_bot in bots:
        new_bot = Bot(token=db_bot.api_token, session=bot.session)
        try:
            await new_bot.get_me()
        except TelegramUnauthorizedError:
            continue
        await new_bot.delete_webhook(drop_pending_updates=True)
        await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=db_bot.api_token))


async def on_shutdown(bots: List[Bot]):
    for bot in bots:
        await on_bot_shutdown(bot)


async def echo(message: types.Message):
    await message.answer(message.text)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    models.Base.metadata.create_all(bind=engine)

    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": ParseMode.HTML}
    bot = Bot(token=MAIN_BOT_TOKEN, **bot_settings)
    storage = MemoryStorage()
    main_dispatcher = Dispatcher(storage=storage)
    main_dispatcher.include_routers(user.router, bots_manage.router, other.router, admin.router)
    main_dispatcher.startup.register(on_startup)

    multibot_dispatcher = Dispatcher(storage=storage)
    multibot_dispatcher.include_routers(dop.user.router, dop.system.router, dop.admin.router)

    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot).register(app, path=MAIN_BOT_PATH)
    TokenBasedRequestHandler(
        dispatcher=multibot_dispatcher,
        bot_settings=bot_settings,
    ).register(app, path=OTHER_BOTS_PATH)

    setup_application(app, main_dispatcher, bot=bot)
    setup_application(app, multibot_dispatcher)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
