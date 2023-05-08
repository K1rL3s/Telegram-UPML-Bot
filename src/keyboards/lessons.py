from datetime import date

from aiogram.types.inline_keyboard import InlineKeyboardMarkup

from src.keyboards.universal import _get_keyboard_for_left_right_menu
from src.utils.consts import CallbackData


def lessons_keyboard(curr_date: date = None) -> InlineKeyboardMarkup:
    return _get_keyboard_for_left_right_menu(
        open_smt_on_callback=CallbackData.OPEN_LESSONS_ON_,
        open_smt_today_callback=CallbackData.OPEN_LESSONS_TODAY,
        today_smile='📔',
        curr_date=curr_date
    )

