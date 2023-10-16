from typing import TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.callbacks import AdminEditData, EditMealData, OpenMenu
from bot.keyboards.admin.admin_manage import open_admins_list_button
from bot.keyboards.universal import go_to_main_menu_button
from bot.utils.enums import Meals, Menus, Roles

if TYPE_CHECKING:
    from bot.database.repository import UserRepository


AUTO_UPDATE_CAFE_MENU = "🍴Загрузить меню"
EDIT_CAFE_MENU = "🍴Изменить меню"
EDIT_LESSONS = "📓Загрузить уроки"
DO_NOTIFY = "🔔Уведомление"
EDIT_EDUCATORS_SCHEDULE = "👩‍✈️Изменить расписание воспитателей"


async def admin_panel_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "InlineKeyboardMarkup":
    """Клавиатура в админ меню."""
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        (
            AUTO_UPDATE_CAFE_MENU,
            EDIT_CAFE_MENU,
            EDIT_LESSONS,
            DO_NOTIFY,
            EDIT_EDUCATORS_SCHEDULE,
        ),
        (
            EditMealData(meal=Meals.AUTO_ALL),
            AdminEditData(menu=Menus.CAFE_MENU),
            AdminEditData(menu=Menus.LESSONS),
            OpenMenu(menu=Menus.NOTIFY),
            AdminEditData(menu=Menus.EDUCATORS),
        ),
    ):
        keyboard.button(text=button_text, callback_data=callback_data)

    if await repo.is_has_any_role(user_id, [Roles.SUPERADMIN]):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    keyboard.adjust(2, 2, 1, 1, repeat=True)

    return keyboard.as_markup()
