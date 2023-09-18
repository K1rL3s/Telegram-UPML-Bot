import datetime as dt
from math import ceil
from typing import TYPE_CHECKING

from bot.keyboards import laundry_keyboard
from bot.utils.consts import LAUNDRY_REPEAT
from bot.utils.enums import UserCallback
from bot.utils.datehelp import datetime_now, datetime_time_delta

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup

    from bot.database.models.laundries import Laundry
    from bot.database.repository import LaundryRepository, SettingsRepository


async def laundry_both_handler(
    user_id: int,
    repo: "LaundryRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Текст и клавиатура при переходе в таймеры для прачечной.

    :param user_id: ТГ Айди.
    :param repo: Репозиторий таймеров прачечной.
    :return: Сообщение пользователю и клавиатура.
    """
    text = f"""Привет! Я - таймер для прачечной.
После конца таймер запустится ещё два раза на <b>{LAUNDRY_REPEAT}</b> минут."""

    laundry = await repo.get(user_id)
    keyboard = await laundry_keyboard(laundry)

    if (minutes := await laundry_time_left(laundry)) is not None:
        text += f"\n\nВремя до конца таймера: <b>~{minutes}</b> минут"

    return text, keyboard


async def laundry_time_left(laundry: "Laundry") -> int | None:
    """
    Возвращает, сколько осталось до конца активного таймера прачечной.

    :param laundry: Модель таймера прачечной.
    :return: Минуты до конца таймера.
    """
    now = datetime_now()

    if (
        not laundry
        or not laundry.is_active
        or not laundry.end_time
        or laundry.end_time < now
    ):
        return None

    delta_time: dt.timedelta = laundry.end_time - now
    return ceil(delta_time.total_seconds() / 60)


async def laundry_start_timer_func(
    settings_repo: "SettingsRepository",
    laundry_repo: "LaundryRepository",
    user_id: int,
    callback_data: str,
) -> tuple[int, "dt.datetime"]:
    """
    Логика обработки кнопок "Запустить стирку" и "Запустить сушку".

    :param settings_repo: Репозиторий настроек.
    :param laundry_repo: Репозиторий таймеров прачечной.
    :param user_id: ТГ Айди.
    :param callback_data: Дата из кнопки для определения - стирка или сушка.
    """
    settings = await settings_repo.get(user_id)

    attr = callback_data.replace(UserCallback.START_LAUNDRY_PREFIX, "")
    start_time = datetime_now()
    if time := getattr(settings, f"{attr}_time"):
        timedelta = datetime_time_delta(start_time, time)
    else:
        timedelta = dt.timedelta(minutes=getattr(settings, f"{attr}_minutes"))

    end_time = start_time + timedelta

    await laundry_repo.save_or_update_to_db(
        user_id,
        start_time=start_time,
        end_time=end_time,
        is_active=True,
        rings=0,
    )

    return timedelta.seconds // 60, end_time


async def laundry_cancel_timer_func(repo: "LaundryRepository", user_id: int) -> None:
    """
    Логика обработчика кнопки "Отменить таймер".

    :param repo: Репозиторий таймеров прачечной.
    :param user_id: ТГ Айди.
    """
    await repo.save_or_update_to_db(
        user_id,
        start_time=None,
        end_time=None,
        is_active=False,
        rings=None,
    )
