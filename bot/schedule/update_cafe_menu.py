from loguru import logger

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.upml.save_cafe_menu import save_cafe_menu
from bot.utils.datehelp import get_this_week_monday


async def update_cafe_menu() -> None:
    async with get_session() as session:
        repo = Repository(session)
        if await repo.menu.get_menu_by_date(get_this_week_monday()):
            return
        status, message = await save_cafe_menu(repo)
        logger.info(f"Обновление меню - {status}, {message}")
