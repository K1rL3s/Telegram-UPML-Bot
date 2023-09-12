from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.keyboards.admin.admin_manage import open_admins_list_button
from bot.keyboards.universal import go_to_main_menu_button
from bot.utils.enums import AdminCallback, Roles


if TYPE_CHECKING:
    from bot.database.repository import UserRepository


SET_CAFE_MENU = "🍴Загрузить меню"
EDIT_CAFE_MENU = "🍴Изменить меню"
SET_LESSONS = "📓Загрузить уроки"
NOTIFY = "🔔Уведомление"
EDIT_EDUCATORS_SCHEDULE = "👩‍✈️Изменить расписание воспитателей"


async def admin_panel_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "InlineKeyboardMarkup":
    """Клавиатура в админ меню."""
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        (
            SET_CAFE_MENU,
            EDIT_CAFE_MENU,
            SET_LESSONS,
            NOTIFY,
            EDIT_EDUCATORS_SCHEDULE,
        ),
        (
            AdminCallback.AUTO_UPDATE_CAFE_MENU,
            AdminCallback.EDIT_CAFE_MENU,
            AdminCallback.UPLOAD_LESSONS,
            AdminCallback.DO_A_NOTIFY_FOR_,
            AdminCallback.EDIT_EDUCATORS,
        ),
    ):
        keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=callback_data),
        )

    if await repo.is_has_any_role(user_id, [Roles.SUPERADMIN]):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    keyboard.adjust(2, 2, 1, 1, repeat=True)

    return keyboard.as_markup()
