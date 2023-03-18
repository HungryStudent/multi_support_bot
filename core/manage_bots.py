from aiogram import Bot, Dispatcher

from polling_manager import PollingManager


async def add_bot(token, dp_for_new_bot: Dispatcher, polling_manager: PollingManager):
    bot = Bot(token)

    polling_manager.start_bot_polling(
        dp=dp_for_new_bot,
        bot=bot,
        polling_manager=polling_manager,
        dp_for_new_bot=dp_for_new_bot,
    )


async def stop_bot(bot_id, polling_manager: PollingManager):
    polling_manager.stop_bot_polling(int(bot_id))
