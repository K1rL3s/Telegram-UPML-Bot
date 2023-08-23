from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.database.repository.repository import Repository
from bot.keyboards.admin.admin_manage import open_admins_list_button
from bot.keyboards.universal import go_to_main_menu_button
from bot.utils.consts import AdminCallback, Roles


async def admin_panel_keyboard(repo: Repository, user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        (
            "🍴Загрузить меню",
            "🍴Изменить меню",
            "📓Загрузить уроки",
            "🔔Уведомление",
            "👩‍✈️Изменить расписание воспитателей",
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
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    if await repo.user.is_has_any_role(user_id, [Roles.SUPERADMIN]):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    keyboard.adjust(2, 2, 1, 1, repeat=True)

    return keyboard.as_markup()
