from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from loguru import logger
from sqlalchemy.orm import close_all_sessions

from bot.handlers import include_routers
from bot.settings import BotSettings
from bot.utils.consts import SLASH_COMMANDS


async def on_startup() -> None:
    pass


async def on_shutdown() -> None:
    close_all_sessions()


async def set_commands(bot: Bot) -> bool:
    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in SLASH_COMMANDS.items()
        ],
        language_code="ru",
    )


def make_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage(), name="__main__")

    include_routers(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def make_bot() -> Bot:
    bot = Bot(token=BotSettings.BOT_TOKEN, parse_mode="markdown")
    await set_commands(bot)

    return bot


def setup_logs() -> None:
    workdir_path = Path(__file__).parent.parent.absolute()

    logger.add(
        workdir_path / "logs" / "logs.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level="DEBUG",
        rotation="00:00",
        compression="zip",
    )
