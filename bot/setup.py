from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from pathlib import Path

from loguru import logger
from sqlalchemy.orm import close_all_sessions

from bot.handlers import include_routers
from bot.middlewares import setup_middlewares
from bot.config import Config
from bot.utils.consts import bot_slash_commands


async def on_startup() -> None:
    pass


async def on_shutdown() -> None:
    close_all_sessions()


async def set_commands(bot: Bot) -> bool:
    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in bot_slash_commands.items()
        ]
    )


def make_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage(), name='__main__')

    include_routers(dp)
    setup_middlewares(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def make_bot() -> Bot:
    bot = Bot(token=Config.BOT_TOKEN, parse_mode='markdown')
    await set_commands(bot)

    return bot


def setup_logs() -> None:
    workdir_path = Path(__file__).parent.parent.absolute()

    logger.add(
        workdir_path / 'logs' / 'logs.log',
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level='DEBUG',
        rotation="00:00",
        compression="zip",
    )
