from typing import TYPE_CHECKING

from bot.keyboards.universal import _keyboard_for_left_right_menu
from bot.utils.enums import UserCallback


if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def cafe_menu_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания столовой с перемоткой влево-вправо по дня."""
    return _keyboard_for_left_right_menu(
        open_smt_on_=UserCallback.OPEN_CAFE_MENU_ON_,
        today_smile="🍴",
        date=date,
    )
