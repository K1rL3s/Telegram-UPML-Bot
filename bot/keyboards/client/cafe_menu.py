from typing import TYPE_CHECKING

from bot.keyboards.universal import _left_right_keyboard_navigation
from shared.utils.enums import Menus

if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def cafe_menu_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания столовой с перемоткой влево-вправо по дня."""
    return _left_right_keyboard_navigation(
        bot_menu=Menus.CAFE_MENU,
        today_smile="🍴",
        date=date,
    )
