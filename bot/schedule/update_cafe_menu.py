from loguru import logger

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.upml.save_cafe_menu import process_cafe_menu
from bot.utils.datehelp import date_today, get_this_week_monday


async def update_cafe_menu(timeout: int) -> None:
    """Автоматическое обновление расписание столовой, используется в aioschedule."""
    async with get_session() as session:
        repo = Repository(session).menu

        monday = await repo.get(get_this_week_monday())
        today = await repo.get(date_today())
        if monday or today:
            return

        status, message = await process_cafe_menu(repo, timeout)
        logger.info(f"Обновление меню - {status}, {message}")
