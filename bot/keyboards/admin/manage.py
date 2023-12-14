from math import ceil

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import AdminCheck, AdminEditRole, AdminList
from bot.keyboards.universal import (
    admin_panel_button,
    cancel_state_button,
    confirm_state_button,
)
from shared.utils.enums import Actions, Roles
from shared.utils.translate import ROLES_TRANSLATE

ADMIN_LIST = "👮‍♀️Список админов"
EDIT_PERMISSIONS = "🔎Изменить роли"
PAGE_BACK = "⬅️Назад"
PAGE_FORWARD = "➡️Вперёд"
ADD_ROLE = "✅Дать"
REMOVE_ROLE = "🚫Снять"

admins_list_button = InlineKeyboardButton(
    text=ADMIN_LIST,
    callback_data=AdminList(page=0).pack(),
)
edit_permissions_button = InlineKeyboardButton(
    text=EDIT_PERMISSIONS,
    callback_data=AdminEditRole(action=Actions.EDIT).pack(),
)


def admins_list_keyboard(
    users: list[tuple[str, int]],
    page: int,
) -> "InlineKeyboardMarkup":
    """
    Клавиатура для просмотра админов.

    :param users: Список с кортежами (имя, айди) об админах.
    :param page: Страница.
    """
    upp = 6  # 6 пользователей на страницу (users per page)
    keyboard = InlineKeyboardBuilder()

    for name, user_id in users[page * upp : page * upp + upp]:
        keyboard.button(
            text=name,
            callback_data=AdminCheck(
                user_id=user_id,
                page=page,
            ),
        )

    if page > 0:
        keyboard.button(
            text=PAGE_BACK,
            callback_data=AdminList(page=page - 1),
        )

    if page * upp + upp < len(users):
        keyboard.button(
            text=PAGE_FORWARD,
            callback_data=AdminList(page=page + 1),
        )

    keyboard.add(
        edit_permissions_button,
        admin_panel_button,
    )

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def check_admin_roles_keyboard(
    user_id: int,
    page: int,
    roles: list[str],
) -> "InlineKeyboardMarkup":
    """
    Клавиатура просмотра одного админа.

    :param user_id: ТГ Айди.
    :param page: Страница списка админов.
    :param roles: Роли администратора.
    :return: Клавиатура.
    """
    keyboard = InlineKeyboardBuilder()
    for role in roles:
        if isinstance(role, Roles):
            role = role.value
        keyboard.button(
            text=ROLES_TRANSLATE[role].capitalize(),
            callback_data=AdminEditRole(
                action=Actions.EDIT,
                user_id=user_id,
                role=role,
            ),
        )

    keyboard.adjust(ceil(len(roles) / 2), repeat=True)
    keyboard.row(
        InlineKeyboardButton(
            text=ADMIN_LIST,
            callback_data=AdminList(page=page).pack(),
        ),
        admin_panel_button,
    )

    return keyboard.as_markup()


def edit_roles_keyboard(
    all_roles: list[str],
    choosed_roles: list[str],
) -> "InlineKeyboardMarkup":
    """
    Клавиатура для множественного выбора (редактирования) ролей.

    :param all_roles: Все отображаемые роли.
    :param choosed_roles: Выбранные роли.
    :return: Клавиатура.
    """
    keyboard = InlineKeyboardBuilder()
    for role in all_roles:
        text = ROLES_TRANSLATE[role].capitalize()
        if role in choosed_roles:
            text = f"🔘{text}"

        keyboard.button(
            text=text,
            callback_data=AdminEditRole(
                role=role,
            ),
        )

    keyboard.adjust(ceil(len(all_roles) / 3) or 1, repeat=True)
    keyboard.row(confirm_state_button, cancel_state_button)

    return keyboard.as_markup()
