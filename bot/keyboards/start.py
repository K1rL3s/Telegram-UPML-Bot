from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.database.db_funcs import Repository
from bot.keyboards.universal import (
    go_to_admin_panel_button,
    go_to_main_menu_button, go_to_settings_button,
)
from bot.utils.consts import CallbackData, Roles


go_to_main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[go_to_main_menu_button]]
)


async def main_menu_keyboard(
        repo: Repository,
        user_id: int
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        ("🍴Меню", "📓Уроки",
         "💦Прачечная", "📖Элективы",
         "👩‍✈️Воспитатели"),
        (CallbackData.OPEN_CAFE_MENU_TODAY, CallbackData.OPEN_LESSONS_TODAY,
         CallbackData.OPEN_LAUNDRY, CallbackData.OPEN_ELECTIVES,
         CallbackData.OPEN_EDUCATORS_TODAY)

    ):
        keyboard.add(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )

    keyboard.add(go_to_settings_button)

    if await repo.is_has_any_role(user_id, [Roles.SUPERADMIN, Roles.ADMIN]):
        keyboard.add(go_to_admin_panel_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
