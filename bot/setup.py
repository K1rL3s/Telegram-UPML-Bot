from pathlib import Path
from typing import Final, TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import close_all_sessions
from loguru import logger

from bot.handlers import include_routers
from bot.utils.enums import SlashCommands


if TYPE_CHECKING:
    from bot.settings import Settings


SETTINGS_KEY: Final[str] = "settings"
SESSION_MAKER_KEY: Final[str] = "session_maker"


async def on_startup() -> None:
    """Код, отрабатывающий при запуске бота."""
    pass


async def on_shutdown() -> None:
    """Код, отрабатывающий при выключении бота."""
    close_all_sessions()


async def set_commands(bot: "Bot") -> bool:
    """Установка команд для бота."""
    commands: dict[str, str] = {
        SlashCommands.START: "Старт",
        SlashCommands.HELP: "Помощь",
        SlashCommands.SETTINGS: "Настройки",
        SlashCommands.MENU: "Меню",
    }

    return await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


def make_dispatcher(
    settings: "Settings",
    session_maker: "async_sessionmaker[AsyncSession]",
    settings_key: str = SETTINGS_KEY,
    session_maker_key: str = SESSION_MAKER_KEY,
) -> "Dispatcher":
    """Создаёт диспетчер и регистрирует все роуты."""
    dp = Dispatcher(storage=MemoryStorage(), name="__main__")

    dp[settings_key] = settings
    dp[session_maker_key] = session_maker

    include_routers(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return dp


async def make_bot(bot_token: str, parse_mode: str = ParseMode.HTML) -> "Bot":
    """Создаёт бота и устанавливает ему команды."""
    bot = Bot(
        token=bot_token,
        parse_mode=parse_mode,
        disable_web_page_preview=True,
    )
    await set_commands(bot)

    return bot


def setup_logs() -> None:
    """Задаёт формат логов и указывает путь записи."""
    workdir_path = Path(__file__).parent.parent.absolute()

    logger.add(
        workdir_path / "logs" / "logs.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        level="DEBUG",
        rotation="00:00",
        compression="zip",
    )
