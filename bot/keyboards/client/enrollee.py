from aiogram.types import InlineKeyboardMarkup

from bot.keyboards.universal import (
    main_menu_button,
    olymps_menu_button,
    univers_menu_button,
)

enrollee_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[univers_menu_button, olymps_menu_button], [main_menu_button]]
)
