from typing import Literal, TYPE_CHECKING

from bot.keyboards import cancel_state_keyboard, settings_keyboard
from bot.utils.consts import LAUNDRY_ENG_TO_RU
from bot.utils.datehelp import (
    format_time,
    hours_minutes_to_minutes,
    minutes_to_hours_minutes,
    time_by_format,
)
from bot.utils.enums import UserCallback
from bot.utils.funcs import laundry_limit_min_max
from bot.utils.phrases import DONT_UNDERSTAND_TIMER, YES

if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup
    from aiogram.fsm.context import FSMContext

    from bot.database.repository import SettingsRepository


async def edit_bool_settings_func(
    repo: "SettingsRepository",
    user_id: int,
    callback_data: str,
) -> None:
    """
    Обработчик нажатия кнопки булевского типа.

    :param repo: Репозиторий настроек.
    :param user_id: Айди юзера.
    :param callback_data: Строка из callback'а (нажатая кнопка).
    """
    attr = callback_data.replace(UserCallback.PREFIX_SWITCH, "")
    settings = await repo.get(user_id)
    await repo.save_or_update_to_db(
        user_id,
        **{attr: not getattr(settings, attr)},
    )


async def edit_grade_setting_func(
    repo: "SettingsRepository",
    user_id: int,
    callback_data: str,
) -> bool:
    """
    Обработчик нажатия кнопки смены класса (выбор класса).

    :param repo: Репозиторий настроек.
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

    await repo.save_or_update_to_db(user_id, grade=grade, letter=letter)
    return True


async def edit_laundry_time_func(
    user_id: int,
    attr: Literal["washing", "drying"],
    text: str,
    state: "FSMContext",
    repo: "SettingsRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Логика обработчика ввода минут для смены таймера прачечной.

    :param user_id: ТГ Айди.
    :param attr: Время стирки или время сушки.
    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :param repo: Репозиторий настроек.
    :return: Сообщение и клавиатура пользователю.
    """
    try:
        if ":" in text:
            time = time_by_format(text)
            text = await edit_laundry_by_time(time, user_id, attr, repo)
        else:
            time = laundry_limit_min_max(hours_minutes_to_minutes(text))
            text = await edit_laundry_by_minutes(time, user_id, attr, repo)
    except ValueError:
        return DONT_UNDERSTAND_TIMER, cancel_state_keyboard

    await state.clear()
    keyboard = await settings_keyboard(repo, user_id)

    return text, keyboard


async def edit_laundry_by_minutes(
    minutes: int,
    user_id: int,
    attr: Literal["washing", "drying"],
    repo: "SettingsRepository",
) -> str:
    await repo.save_or_update_to_db(
        user_id, **{
            f"{attr}_minutes": minutes,
            f"{attr}_time": None,
        }
    )

    hours, minutes = minutes_to_hours_minutes(minutes)
    return (
        f"{YES} <b>{LAUNDRY_ENG_TO_RU[attr].capitalize()}</b> "
        f"установлено на <b>{hours} часов, {minutes} минут</b>."
    )


async def edit_laundry_by_time(
    time: "dt.time",
    user_id: int,
    attr: Literal["washing", "drying"],
    repo: "SettingsRepository",
) -> str:
    await repo.save_or_update_to_db(user_id, **{f"{attr}_time": time})

    return (
        f"{YES} <b>{LAUNDRY_ENG_TO_RU[attr].capitalize()}</b> "
        f"установлено на {format_time(time)}."
    )
