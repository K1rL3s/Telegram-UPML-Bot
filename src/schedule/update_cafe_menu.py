from loguru import logger

from src.database.db_funcs import get_menu_by_date
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.datehelp import get_this_week_monday


async def update_cafe_menu() -> None:
    if get_menu_by_date(get_this_week_monday()):
        return
    status, message = await save_cafe_menu()
    logger.info(f"Обновление меню - {status}, {message}")
