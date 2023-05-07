from datetime import date, timedelta

from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from src.utils.consts import CallbackData
from src.utils.dateformat import format_date


def cafe_menu_keyboard(menu_date: date = None) -> InlineKeyboardMarkup:
    today = date.today()

    if menu_date is None:
        menu_date = date.today()

    tomorrow = menu_date + timedelta(days=1)
    yesterday = menu_date - timedelta(days=1)
    tomorrow_str = format_date(tomorrow)
    yesterday_str = format_date(yesterday)

    keyboard = InlineKeyboardMarkup()

    if abs((today - yesterday).days) < 7:
        keyboard.insert(
            InlineKeyboardButton(
                f'⬅️{yesterday_str}',
                callback_data=CallbackData.OPEN_CAFE_MENU_ON_ + yesterday_str
            )
        )

    keyboard.insert(
        InlineKeyboardButton(
            f'🍴Сегодня',
            callback_data=CallbackData.OPEN_TODAY_CAFE_MENU
        )
    )

    if abs((today - tomorrow).days) < 7:
        keyboard.insert(
            InlineKeyboardButton(
                f'➡️{tomorrow_str}',
                callback_data=CallbackData.OPEN_CAFE_MENU_ON_ + tomorrow_str
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            "🏠Главное меню",
            callback_data=CallbackData.OPEN_MAIN_MENU
        )
    )

    return keyboard
