from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.callbacks import AdminEditMenu, EditMeal, OpenMenu
from bot.keyboards.admin.manage import admins_list_button
from bot.keyboards.universal import main_menu_button
from shared.database.repository import UserRepository
from shared.utils.enums import BotMenu, Meal, RoleEnum

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
    is_admin = RoleEnum.SUPERADMIN in roles or RoleEnum.ADMIN in roles

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
            EditMeal(meal=Meal.AUTO_ALL),
            AdminEditMenu(menu=BotMenu.CAFE_MENU),
            AdminEditMenu(menu=BotMenu.LESSONS),
            OpenMenu(menu=BotMenu.NOTIFY),
            AdminEditMenu(menu=BotMenu.EDUCATORS),
        ),
        (
            RoleEnum.CAFE_MENU in roles,
            RoleEnum.CAFE_MENU in roles,
            RoleEnum.LESSONS in roles,
            RoleEnum.NOTIFY in roles,
            RoleEnum.EDUCATORS in roles,
        ),
    ):
        if condition or is_admin:
            keyboard.button(text=text, callback_data=callback_data)

    if RoleEnum.SUPERADMIN in roles:
        keyboard.add(admins_list_button)

    keyboard.add(main_menu_button)

    keyboard.adjust(2, 2, 1, 1, repeat=True)

    return keyboard.as_markup()
