import datetime as dt
from math import ceil
from typing import TYPE_CHECKING

from bot.utils.enums import UserCallback
from bot.utils.datehelp import datetime_now

if TYPE_CHECKING:
    from bot.database.models.laundries import Laundry
    from bot.database.repository import LaundryRepository, SettingsRepository


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

    minutes = getattr(
        settings,
        callback_data.replace(UserCallback.START_LAUNDRY_PREFIX, ""),
    )
    start_time = datetime_now()
    end_time = start_time + dt.timedelta(minutes=minutes)

    await laundry_repo.save_or_update_to_db(
        user_id,
        start_time=start_time,
        end_time=end_time,
        is_active=True,
        rings=0,
    )

    return minutes, end_time


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
