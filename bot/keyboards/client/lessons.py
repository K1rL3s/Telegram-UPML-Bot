from typing import TYPE_CHECKING

from bot.keyboards.universal import _left_right_keyboard_navigation
from bot.utils.enums import Menus

if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def lessons_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания уроков с перемоткой влево-вправо по дня."""
    return _left_right_keyboard_navigation(
        bot_menu=Menus.LESSONS,
        today_smile="📓",
        date=date,
    )
