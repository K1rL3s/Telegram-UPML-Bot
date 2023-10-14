from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import AdminListData, AdminManageData
from bot.keyboards.universal import go_to_admin_panel_button
from bot.utils.enums import Actions


ADMIN_LIST = "👮‍♀️Список админов"
ADD_ADMIN = "🔎Добавить админа"
PAGE_BACK = "⬅️Назад"
PAGE_FORWARD = "➡️Вперёд"
REMOVE_ROLE = "🚫Снять роль админа"
REMOVE_ROLE_SURE = "🚫Точно снять роль"


open_admins_list_button = InlineKeyboardButton(
    text=ADMIN_LIST,
    callback_data=AdminListData(page=0).pack(),
)
add_new_admin_button = InlineKeyboardButton(
    text=ADD_ADMIN,
    callback_data=AdminManageData(action=Actions.ADD).pack(),
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
            callback_data=AdminManageData(
                action=Actions.CHECK,
                user_id=user_id,
                page=page,
            ),
        )

    if page > 0:
        keyboard.button(
            text=PAGE_BACK,
            callback_data=AdminListData(page=page - 1),
        )

    if page * upp + upp < len(users):
        keyboard.button(
            text=PAGE_FORWARD,
            callback_data=AdminListData(page=page + 1),
        )

    keyboard.add(
        add_new_admin_button,
        go_to_admin_panel_button,
    )

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


def check_admin_keyboard(
    user_id: int,
    page: int,
    is_sure: bool = False,
) -> "InlineKeyboardMarkup":
    """
    Клавиатура просмотра одного админа.

    :param user_id: ТГ Айди.
    :param page: Страница списка админов.
    :param is_sure: Уверенность в снятии роли.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=REMOVE_ROLE_SURE if is_sure else REMOVE_ROLE,
        callback_data=AdminManageData(
            action=Actions.REMOVE,
            user_id=user_id,
            is_sure=is_sure,
            page=page,
        ),
    )
    keyboard.button(
        text=ADMIN_LIST,
        callback_data=AdminListData(page=page),
    )
    keyboard.add(go_to_admin_panel_button)

    return keyboard.adjust(1, 2).as_markup()
