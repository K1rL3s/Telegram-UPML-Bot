from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.database.repository.repository import Repository
from bot.upml.save_cafe_menu import process_cafe_menu
from bot.utils.datehelp import date_today, get_this_week_monday


async def update_cafe_menu(
    session_maker: "async_sessionmaker[AsyncSession]",
    timeout: int,
) -> None:
    """Автоматическое обновление расписание столовой, используется в apscheduler."""
    async with session_maker() as session:
        repo = Repository(session).menu

        monday = await repo.get(get_this_week_monday())
        today = await repo.get(date_today())
        if monday or today:
            return

        await process_cafe_menu(repo, timeout)
