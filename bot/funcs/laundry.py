import datetime as dt
from math import ceil
from typing import TYPE_CHECKING

from bot.utils.consts import UserCallback
from bot.utils.datehelp import datetime_now

if TYPE_CHECKING:
    from bot.database.repository.repository import Repository
    from bot.database.models.laundries import Laundry


async def laundry_welcome_func(laundry: "Laundry") -> int | None:
    """
    Логика обработчика кнопки "Прачечная".

    :param laundry: Модель таймера прачечной.
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
    repo: "Repository",
    user_id: int,
    callback_data: str,
) -> tuple[int, "dt.datetime"]:
    """
    Логика обработки кнопок "Запустить стирку" и "Запустить сушку".

    :param repo: Доступ к базе данных.
    :param user_id: ТГ Айди.
    :param callback_data: Дата из кнопки для определения - стирка или сушка.
    """
    settings = await repo.settings.get(user_id)

    minutes = getattr(
        settings,
        callback_data.replace(UserCallback.START_LAUNDRY_PREFIX, ""),
    )
    start_time = datetime_now()
    end_time = start_time + dt.timedelta(minutes=minutes)

    await repo.laundry.save_or_update_to_db(
        user_id,
        start_time=start_time,
        end_time=end_time,
        is_active=True,
    )

    return minutes, end_time


async def laundry_cancel_timer_func(repo: "Repository", user_id: int) -> None:
    """
    Логика обработчика кнопки "Отменить таймер".

    :param repo: Доступ к базе данных.
    :param user_id: ТГ Айди.
    """
    await repo.laundry.save_or_update_to_db(
        user_id,
        start_time=None,
        end_time=None,
        is_active=False,
        rings=None,
    )
