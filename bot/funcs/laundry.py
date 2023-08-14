from math import ceil
from datetime import datetime, timedelta

from bot.database.db_funcs import Repository
from bot.database.models.laundries import Laundry
from bot.utils.consts import CallbackData
from bot.utils.datehelp import datetime_now


async def laundry_welcome_func(laundry: Laundry) -> int | None:
    """
    Логика обработчика кнопки "Прачечная".
    """
    now = datetime_now()

    if (
            not laundry
            or not laundry.is_active
            or not laundry.end_time
            or laundry.end_time < now
    ):
        return None

    delta_time: timedelta = laundry.end_time - now
    return ceil(delta_time.total_seconds() / 60)


async def laundry_start_timer_func(
        repo: Repository,
        user_id: int,
        callback_data: str
) -> tuple[int, datetime]:
    """
    Логика обработки кнопок "Запустить стирку" и "Запустить сушку".
    """
    settings = await repo.get_settings(user_id)

    minutes = getattr(
        settings, callback_data.replace(CallbackData.START_LAUNDRY_PREFIX, '')
    )
    start_time = datetime_now()
    end_time = start_time + timedelta(minutes=minutes)

    await repo.save_or_update_laundry(
        user_id, start_time=start_time, end_time=end_time, is_active=True
    )

    return minutes, end_time


async def laundry_cancel_timer_func(
        repo: Repository,
        user_id: int
) -> None:
    """
    Логика обработчика кнопки "Отменить таймер".
    """
    await repo.save_or_update_laundry(
        user_id, start_time=None, end_time=None, is_active=False, rings=None
    )
