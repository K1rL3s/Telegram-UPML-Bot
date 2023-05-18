from src.database.db_funcs import (
    get_settings, save_or_update_settings,
)
from src.database.models.settings import Settings
from src.utils.consts import CallbackData
from src.utils.funcs import limit_min_max


def edit_bool_settings_handler(
        user_id: int,
        callback_data: str,
) -> None:
    """
    Обработчик нажатия кнопки булевского типа.

    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    :return: Параметры для клавиатуры.
    """

    attr = callback_data.replace(CallbackData.PREFIX_SWITCH, '')
    settings = get_settings(user_id)
    save_or_update_settings(user_id, **{attr: not getattr(settings, attr)})

    # return get_settings(user_id)


def edit_grade_setting_handler(
        user_id: int,
        callback_data: str,
) -> Settings | None:
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
        save_or_update_settings(user_id, grade=None, letter=None)
    else:
        save_or_update_settings(user_id, grade=grade[:2], letter=grade[-1:])

    return get_settings(user_id)


def edit_laundry_time_handler(user_id: int, attr: str, text: str) -> int:
    try:
        minutes = limit_min_max(int(text), 1, 2 * 24 * 60)  # двое суток
        save_or_update_settings(user_id, **{attr: minutes})
        return minutes
    except ValueError:
        return 0
