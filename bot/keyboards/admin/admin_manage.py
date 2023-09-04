from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.keyboards.universal import (
    cancel_state_button,
    go_to_admin_panel_button,
)
from bot.utils.enums import AdminCallback


open_admins_list_button = InlineKeyboardButton(
    text="👮‍♀️Список админов",
    callback_data=AdminCallback.OPEN_ADMINS_LIST_PAGE_,
)
add_new_admin_button = InlineKeyboardButton(
    text="🔎Добавить админа",
    callback_data=AdminCallback.ADD_NEW_ADMIN,
)
add_new_admin_sure_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅Подтвердить",
                callback_data=AdminCallback.ADD_NEW_ADMIN_SURE,
            ),
            cancel_state_button,
        ],
    ],
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
        keyboard.add(
            InlineKeyboardButton(
                text=name,
                callback_data=AdminCallback.CHECK_ADMIN_ + f"{user_id}_{page}",
            ),
        )

    if page > 0:
        keyboard.add(
            InlineKeyboardButton(
                text="⬅️Назад",
                callback_data=AdminCallback.OPEN_ADMINS_LIST_PAGE_ + f"{page - 1}",
            ),
        )

    if page * upp + upp < len(users):
        keyboard.add(
            InlineKeyboardButton(
                text="➡️Вперёд",
                callback_data=AdminCallback.OPEN_ADMINS_LIST_PAGE_ + f"{page + 1}",
            ),
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
    sure: bool = False,
) -> "InlineKeyboardMarkup":
    """
    Клавиатура просмотра одного админа.

    :param user_id: ТГ Айди.
    :param page: Страница списка админов.
    :param sure: Уверенность в снятии роли.
    """
    remove_button = InlineKeyboardButton(
        text="🚫Точно снять роль" if sure else "🚫Снять роль админа",
        callback_data=(
            AdminCallback.REMOVE_ADMIN_SURE_ + f"{user_id}_{page}"
            if sure
            else AdminCallback.REMOVE_ADMIN_ + f"{user_id}_{page}"
        ),
    )
    return (
        InlineKeyboardBuilder()
        .add(remove_button)
        .add(
            go_to_admin_panel_button,
            InlineKeyboardButton(
                text="👨‍✈️Список админов",
                callback_data=AdminCallback.OPEN_ADMINS_LIST_PAGE_ + f"{page}",
            ),
        )
        .adjust(1, 2)
        .as_markup()
    )
