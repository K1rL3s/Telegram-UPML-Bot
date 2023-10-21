from typing import TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.callbacks import AdminEditMenu, EditMeal, OpenMenu
from bot.keyboards.admin.manage import admins_list_button
from bot.keyboards.universal import main_menu_button
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
    roles: list[str] = [role.role for role in (await repo.get(user_id)).roles]
    is_admin = Roles.SUPERADMIN in roles or Roles.ADMIN in roles

    keyboard = InlineKeyboardBuilder()
    for text, callback_data, condition in zip(
        (
            AUTO_UPDATE_CAFE_MENU,
            EDIT_CAFE_MENU,
            EDIT_LESSONS,
            DO_NOTIFY,
            EDIT_EDUCATORS_SCHEDULE,
        ),
        (
            EditMeal(meal=Meals.AUTO_ALL),
            AdminEditMenu(menu=Menus.CAFE_MENU),
            AdminEditMenu(menu=Menus.LESSONS),
            OpenMenu(menu=Menus.NOTIFY),
            AdminEditMenu(menu=Menus.EDUCATORS),
        ),
        (
            Roles.CAFE_MENU in roles,
            Roles.CAFE_MENU in roles,
            Roles.LESSONS in roles,
            Roles.NOTIFY in roles,
            Roles.EDUCATORS in roles,
        ),
    ):
        if condition or is_admin:
            keyboard.button(text=text, callback_data=callback_data)

    if Roles.SUPERADMIN in roles:
        keyboard.add(admins_list_button)

    keyboard.add(main_menu_button)

    keyboard.adjust(2, 2, 1, 1, repeat=True)

    return keyboard.as_markup()
