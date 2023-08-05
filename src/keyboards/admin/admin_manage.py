from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.keyboards.universal import (
    cancel_state_button,
    go_to_admin_panel_button,
)
from src.utils.consts import CallbackData


open_admins_list_button = InlineKeyboardButton(
    text='👮‍♀️Список админов',
    callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_
)
add_new_admin_button = InlineKeyboardButton(
    text='🔎Добавить админа',
    callback_data=CallbackData.ADD_NEW_ADMIN
)
add_new_admin_sure_keyboard = InlineKeyboardBuilder().add(
    InlineKeyboardButton(
        text='✅Подтвердить',
        callback_data=CallbackData.ADD_NEW_ADMIN_SURE
    ),
    cancel_state_button
).as_markup()


def admins_list_keyboard(
        users: list[tuple[str, int]],
        page: int
) -> InlineKeyboardMarkup:
    upp = 6  # 6 пользователей на страницу (users per page)
    keyboard = InlineKeyboardBuilder()

    for name, user_id in users[page * upp:page * upp + upp]:
        keyboard.add(
            InlineKeyboardButton(
                text=name,
                callback_data=CallbackData.CHECK_ADMIN_ + f'{user_id}_{page}'
            )
        )

    if page > 0:
        keyboard.add(
            InlineKeyboardButton(
                text=f'⬅️Назад',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page - 1}'
            )
        )

    if page * upp + upp < len(users):
        keyboard.add(
            InlineKeyboardButton(
                text=f'➡️Вперёд',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page + 1}'
            )
        )

    keyboard.add(
        go_to_admin_panel_button,
        add_new_admin_button
    )

    return keyboard.as_markup()


def check_admin_keyboard(
        user_id: int,
        page: int,
        sure: bool = False
) -> InlineKeyboardMarkup:
    remove_button = InlineKeyboardButton(
        text=("🚫Точно снять роль" if sure else "🚫Снять роль админа"),
        callback_data=(
            CallbackData.REMOVE_ADMIN_SURE_ + f'{user_id}'
            if sure else
            CallbackData.REMOVE_ADMIN_ + f'{user_id}_{page}'
        )
    )
    return InlineKeyboardBuilder().add(
        remove_button
    ).add(
        go_to_admin_panel_button,
        InlineKeyboardButton(
            text=f'👨‍✈️Список админов',
            callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page}'
        )
    ).as_markup()
