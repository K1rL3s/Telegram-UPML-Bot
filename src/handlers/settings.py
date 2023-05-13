from src.database.db_funcs import (
    get_user, save_user_or_update_status,
    update_user,
)
from src.utils.consts import CallbackData


def open_settings_handler(
        user_id: int,
        username: str
) -> tuple[str | None, str | None, bool, bool]:
    """
    Обработчик открытия настроек.

    :param user_id: Айди юзера.
    :param username: Имя юзера.
    :return: Параметры для клавиатуры.
    """

    user = get_user(user_id)

    if user is None:
        save_user_or_update_status(user_id, username)
        user = get_user(user_id)

    return user.grade, user.letter, user.lessons_notify, user.news_notify


def edit_bool_settings_handler(
        user_id: int,
        callback_data: str,
) -> tuple[str | None, str | None, bool, bool]:
    """
    Обработчик нажатия кнопки булевского типа.

    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    :return: Параметры для клавиатуры.
    """

    attr = callback_data.replace(CallbackData.PREFIX_SWITCH, '')
    user = get_user(user_id)
    update_user(user_id, **{attr: not getattr(user, attr)})

    user = get_user(user_id)

    return user.grade, user.letter, user.lessons_notify, user.news_notify


def edit_grade_setting_handler(
        user_id: int,
        callback_data: str,
) -> tuple[str | None, str | None, bool, bool] | None:
    """
    Обработчик нажатия кнопки смены класса (выбор класса).

    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    :return: Параметры для клавиатуры.
    """

    grade = callback_data.replace(CallbackData.CHANGE_GRADE_TO_, '')

    if not grade:
        return None

    if grade.lower() == 'none':
        update_user(user_id, grade=None, letter=None)
    else:
        update_user(user_id, grade=grade[:2], letter=grade[-1:])

    user = get_user(user_id)

    return user.grade, user.letter, user.lessons_notify, user.news_notify
