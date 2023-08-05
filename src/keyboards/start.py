from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.database.db_funcs import is_has_any_role
from src.keyboards.universal import (
    go_to_admin_panel_button,
    go_to_main_menu_button, go_to_settings_button,
)
from src.utils.consts import CallbackData, Roles


go_to_main_menu_keyboard = InlineKeyboardBuilder().add(
    go_to_main_menu_button
).as_markup()


def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="🍴Меню",
            callback_data=CallbackData.OPEN_CAFE_MENU_TODAY
        ),
        InlineKeyboardButton(
            text="📓Уроки",
            callback_data=CallbackData.OPEN_LESSONS_TODAY
        )
    ).add(
        InlineKeyboardButton(
            text='💦Прачечная',
            callback_data=CallbackData.OPEN_LAUNDRY
        ),
        InlineKeyboardButton(
            text='📖Элективы',
            callback_data=CallbackData.OPEN_ELECTIVES
        ),
    ).add(
        InlineKeyboardButton(
            text='👩‍✈️Воспитатели',
            callback_data=CallbackData.OPEN_EDUCATORS
        ),
        go_to_settings_button
    )

    if is_has_any_role(user_id, [Roles.SUPERADMIN, Roles.ADMIN]):
        keyboard.add(go_to_admin_panel_button)

    return keyboard.as_markup()
