import datetime as dt

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.universal import _left_right_keyboard_navigation
from shared.utils.enums import BotMenu


def educators_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания воспитателей с перемоткой влево-вправо по дням."""
    return _left_right_keyboard_navigation(
        menu=BotMenu.EDUCATORS,
        today_smile="👩‍✈️",
        date=date,
    )
