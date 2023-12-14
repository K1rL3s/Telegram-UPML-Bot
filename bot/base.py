import datetime as dt
from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from loguru import logger
from sqlalchemy.orm import close_all_sessions

from bot.handlers import include_routers
from shared.utils.enums import SlashCommands

if TYPE_CHECKING:
    from redis.asyncio import Redis

    from shared.core.settings import Settings


async def on_startup(bot: "Bot") -> None:
    """Код, отрабатывающий при запуске бота."""
    user = await bot.me()  # Copypaste from aiogram
    logger.info(
        "Start polling for bot @{username} id={id} - '{full_name}'",
        username=user.username,
        id=user.id,
        full_name=user.full_name,
    )  # Copypaste from aiogram


async def on_shutdown(bot: "Bot", redis: "Redis") -> None:
    """Код, отрабатывающий при выключении бота."""
    await redis.close()
    close_all_sessions()

    user = await bot.me()
    logger.info(
        "Stop polling for bot @{username} id={id} - '{full_name}'",
        username=user.username,
        id=user.id,
        full_name=user.full_name,
    )


async def set_commands(bot: "Bot") -> bool:
    """Установка команд для бота."""
    commands: dict[str, str] = {
        SlashCommands.START: "Старт",
        SlashCommands.HELP: "Помощь",
        SlashCommands.MENU: "Меню",
        SlashCommands.SETTINGS: "Настройки",
        SlashCommands.CANCEL: "Отмена ввода",
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
    redis: "Redis",
) -> "Dispatcher":
    """Создаёт диспетчер и регистрирует все роуты."""
    dp = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            state_ttl=dt.timedelta(days=1),
            data_ttl=dt.timedelta(days=1),
        ),
        redis=redis,
        settings=settings,
        name="__main__",
    )

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
