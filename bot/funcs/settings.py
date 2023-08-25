from typing import Literal, TYPE_CHECKING

from bot.utils.consts import UserCallback
from bot.utils.funcs import limit_min_max

if TYPE_CHECKING:
    from bot.database.repository.repository import Repository


async def edit_bool_settings_func(
    repo: "Repository",
    user_id: int,
    callback_data: str,
) -> None:
    """
    Обработчик нажатия кнопки булевского типа.

    :param repo: Доступ к базе данных.
    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    """
    attr = callback_data.replace(UserCallback.PREFIX_SWITCH, "")
    settings = await repo.settings.get(user_id)
    await repo.settings.save_or_update_to_db(
        user_id,
        **{attr: not getattr(settings, attr)},
    )


async def edit_grade_setting_func(
    repo: "Repository",
    user_id: int,
    callback_data: str,
) -> bool:
    """
    Обработчик нажатия кнопки смены класса (выбор класса).

    :param repo: Доступ к базе данных.
    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    :return: Случилось ли изменение класса.
    """
    if not (grade := callback_data.replace(UserCallback.CHANGE_GRADE_TO_, "")):
        return False

    if grade.lower() == "none":
        grade = letter = None
    else:
        grade, letter = grade[:2], grade[-1:]

    await repo.settings.save_or_update_to_db(user_id, grade=grade, letter=letter)
    return True


async def edit_laundry_time_func(
    repo: "Repository",
    user_id: int,
    attr: Literal["washing_time", "drying_time"],
    text: str,
) -> int:
    """
    Логика обработчика ввода минут для смены таймера прачечной.

    :param repo: Доступ к базе данных.
    :param user_id: ТГ Айди.
    :param attr: Время стирки или время сушки.
    :param text: Сообщение пользователя.
    """
    try:
        minutes = limit_min_max(int(float(text)), 1, 2 * 24 * 60)  # двое суток
        await repo.settings.save_or_update_to_db(user_id, **{attr: minutes})
    except ValueError:
        return 0

    return minutes
