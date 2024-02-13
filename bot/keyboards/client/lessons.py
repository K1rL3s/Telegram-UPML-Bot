import datetime as dt

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.universal import _left_right_keyboard_navigation
from shared.utils.enums import BotMenu


def lessons_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания уроков с перемоткой влево-вправо по днямА."""
    return _left_right_keyboard_navigation(
        menu=BotMenu.LESSONS,
        today_smile="📓",
        date=date,
    )
