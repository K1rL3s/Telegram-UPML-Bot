import datetime as dt

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.universal import _left_right_keyboard_navigation
from shared.utils.enums import BotMenu


def cafe_menu_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания столовой с перемоткой влево-вправо по дням."""
    return _left_right_keyboard_navigation(
        menu=BotMenu.CAFE_MENU,
        today_smile="🍴",
        date=date,
    )
