from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData


start_menu_keyboard = InlineKeyboardMarkup().add(
    go_to_main_menu_button
)

main_menu_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        "🍴Меню",
        callback_data=CallbackData.OPEN_CAFE_MENU_TODAY
    ),
    InlineKeyboardButton(
        "📓Уроки",
        callback_data=CallbackData.OPEN_LESSONS_TODAY
    ),
    InlineKeyboardButton(
        "⚙️Настройки",
        callback_data=CallbackData.OPEN_SETTINGS
    )
)
