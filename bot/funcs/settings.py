from bot.database.db_funcs import Repository
from bot.utils.consts import CallbackData
from bot.utils.funcs import limit_min_max


async def edit_bool_settings_func(
        repo: Repository,
        user_id: int,
        callback_data: str,
) -> None:
    """
    Обработчик нажатия кнопки булевского типа.

    :param repo: Доступ к базе данных.
    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    :return: Параметры для клавиатуры.
    """

    attr = callback_data.replace(CallbackData.PREFIX_SWITCH, '')
    settings = await repo.get_settings(user_id)
    await repo.save_or_update_settings(
        user_id,
        **{attr: not getattr(settings, attr)}
    )

    # return get_settings(user_id)


async def edit_grade_setting_func(
        repo: Repository,
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

    grade = callback_data.replace(CallbackData.CHANGE_GRADE_TO_, '')

    if not grade:
        return False

    if grade.lower() == 'none':
        grade = letter = None
    else:
        grade, letter = grade[:2], grade[-1:]

    await repo.save_or_update_settings(user_id, grade=grade, letter=letter)
    return True


async def edit_laundry_time_func(
        repo: Repository,
        user_id: int,
        attr: str,
        text: str
) -> int:
    try:
        minutes = limit_min_max(int(float(text)), 1, 2 * 24 * 60)  # двое суток
        await repo.save_or_update_settings(user_id, **{attr: minutes})
        return minutes
    except ValueError:
        return 0