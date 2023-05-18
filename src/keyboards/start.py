from aiogram.types.inline_keyboard import (
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from src.database.db_funcs import is_has_any_role
from src.keyboards.universal import (
    go_to_admin_panel_button,
    go_to_main_menu_button, go_to_settings_button,
)
from src.utils.consts import CallbackData, Roles


go_to_main_menu_keyboard = InlineKeyboardMarkup().add(
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
        )
    ).add(
        InlineKeyboardButton(
            '💦Прачечная',
            callback_data=CallbackData.OPEN_LAUNDRY
        ),
        go_to_settings_button
    )

    if is_has_any_role(user_id, [Roles.SUPERADMIN, Roles.ADMIN]):
        keyboard.add(go_to_admin_panel_button)

    return keyboard
