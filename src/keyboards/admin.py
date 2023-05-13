from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.db_funcs import is_has_role
from src.keyboards.universal import (
    go_to_admin_menu_button,
    go_to_main_menu_button,
)
from src.utils.consts import CallbackData, Roles


cancel_state_button = InlineKeyboardButton(
    '❌Отмена',
    callback_data=CallbackData.CANCEL_STATE
)

cancel_state_keyboard = InlineKeyboardMarkup().add(
    cancel_state_button
)
open_admins_list_button = InlineKeyboardButton(
    '👮‍♀️Список админов',
    callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_
)
add_new_admin_button = InlineKeyboardButton(
    '🔎Добавить админа',
    callback_data=CallbackData.ADD_NEW_ADMIN
)

add_new_admin_sure_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        '✅Подтвердить',
        callback_data=CallbackData.ADD_NEW_ADMIN_SURE
    ),
    cancel_state_button
)

choose_meal_keyboard = InlineKeyboardMarkup(row_width=3)
for dish, callback_data in zip(
    ('Завтрак', 'Второй завтрак', 'Обед', 'Полдник', 'Ужин'),
    (
            CallbackData.EDIT_BREAKFAST, CallbackData.EDIT_LUNCH,
            CallbackData.EDIT_DINNER, CallbackData.EDIT_SNACK,
            CallbackData.EDIT_SUPPER
    )
):
    choose_meal_keyboard.insert(
        InlineKeyboardButton(dish, callback_data=callback_data)
    )
choose_meal_keyboard.add(cancel_state_button)

confirm_edit_menu_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        '✅Подтвердить',
        callback_data=CallbackData.EDIT_CONFIRM
    ),
    cancel_state_button
)


def admin_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            '🍴Загрузить меню',
            callback_data=CallbackData.AUTO_UPDATE_CAFE_MENU
        ),
        InlineKeyboardButton(
            '🍴Изменить меню',
            callback_data=CallbackData.MANUAL_EDIT_CAFE_MENU
        ),
    ).add(
        InlineKeyboardButton(
            '📓Загрузить уроки',
            callback_data=CallbackData.UPLOAD_LESSONS
        ),
        InlineKeyboardButton(
            '🔔Уведомление',
            callback_data=CallbackData.DO_A_NOTIFY_FOR_
        ),
    )

    if is_has_role(user_id, Roles.SUPERADMIN):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    return keyboard


def admins_list_keyboard(
        users: list[tuple[str, int]],
        page: int
) -> InlineKeyboardMarkup:
    upp = 6  # 6 пользователей на страницу (users per page)
    keyboard = InlineKeyboardMarkup(row_width=2)

    for name, user_id in users[page * upp:page * upp + upp]:
        keyboard.insert(
            InlineKeyboardButton(
                name,
                callback_data=CallbackData.CHECK_ADMIN_ + f'{user_id}_{page}'
            )
        )

    if page > 0:
        keyboard.add(
            InlineKeyboardButton(
                f'⬅️Назад',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page - 1}'
            )
        )

    if page * upp + upp < len(users):
        keyboard.insert(
            InlineKeyboardButton(
                f'➡️Вперёд',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page + 1}'
            )
        )

    keyboard.add(
        go_to_admin_menu_button,
        add_new_admin_button
    )

    return keyboard


def check_admin_keyboard(
        user_id: int,
        page: int,
        sure: bool = False
) -> InlineKeyboardMarkup:
    remove_button = InlineKeyboardButton(
        "🚫Точно снять роль" if sure else "🚫Снять роль админа",
        callback_data=(
            CallbackData.REMOVE_ADMIN_SURE_ + f'{user_id}'
            if sure else
            CallbackData.REMOVE_ADMIN_ + f'{user_id}_{page}'
        )
    )
    return InlineKeyboardMarkup().add(
        remove_button
    ).add(
        go_to_admin_menu_button,
        InlineKeyboardButton(
            f'👨‍✈️Список админов',
            callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page}'
        )
    )
