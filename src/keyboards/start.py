from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup
)

from src.utils.consts import CallbackData


start_menu_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        "🍴Меню в столовой",
        callback_data=CallbackData.OPEN_TODAY_CAFE_MENU
    )
)
