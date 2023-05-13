from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from src.database.db_funcs import is_has_role
from src.keyboards.universal import (
    go_to_admin_panel_button,
    go_to_main_menu_button,
)
from src.utils.consts import CallbackData, Roles


start_menu_keyboard = InlineKeyboardMarkup().add(
    go_to_main_menu_button
)


def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
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

    if is_has_role(user_id, Roles.ADMIN):
        keyboard.add(go_to_admin_panel_button)

    return keyboard
