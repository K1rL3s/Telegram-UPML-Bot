from datetime import date

from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.universal import _keyboard_for_left_right_menu
from bot.utils.consts import UserCallback


def educators_keyboard(curr_date: date = None) -> InlineKeyboardMarkup:
    return _keyboard_for_left_right_menu(
        open_smt_on_callback=UserCallback.OPEN_EDUCATORS_ON_,
        open_smt_today_callback=UserCallback.OPEN_EDUCATORS_TODAY,
        today_smile="👩‍✈️",
        curr_date=curr_date,
    )
