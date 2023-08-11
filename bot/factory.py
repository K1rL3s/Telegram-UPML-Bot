from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers import include_routers
from bot.middlewares import setup_middlewares
from bot.config import Config
from bot.utils.consts import bot_commands


async def set_commands(bot: Bot) -> bool:
    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in bot_commands.items()
        ],
        language_code='ru'
    )


def make_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage(), name='__main__')

    include_routers(dp)
    setup_middlewares(dp)

    return dp


async def make_bot() -> Bot:
    bot = Bot(token=Config.BOT_TOKEN, parse_mode='markdown')
    await set_commands(bot)

    return bot
