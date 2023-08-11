from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.database.db_funcs import Repository
from bot.keyboards.admin.admin_manage import open_admins_list_button
from bot.keyboards.universal import go_to_main_menu_button
from bot.utils.consts import CallbackData, Roles


async def admin_panel_keyboard(
        repo: Repository,
        user_id: int
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        ('🍴Загрузить меню', '🍴Изменить меню',
         '📓Загрузить уроки', '🔔Уведомление'),
        (CallbackData.AUTO_UPDATE_CAFE_MENU,
         CallbackData.EDIT_CAFE_MENU,
         CallbackData.UPLOAD_LESSONS, CallbackData.DO_A_NOTIFY_FOR_)
    ):
        keyboard.add(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )

    if await repo.is_has_any_role(user_id, [Roles.SUPERADMIN]):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    keyboard.adjust(2, 2, 1, repeat=True)

    return keyboard.as_markup()
