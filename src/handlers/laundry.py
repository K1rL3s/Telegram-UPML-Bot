from math import ceil
from datetime import datetime, timedelta

from src.database.db_funcs import (
    get_laundry, get_settings,
    save_or_update_laundry,
)
from src.utils.consts import CallbackData
from src.utils.datehelp import datetime_now


def laundry_welcome_handler(user_id: int) -> int | None:
    """
    Логика обработчика кнопки "Прачечная".
    """
    laundry = get_laundry(user_id)

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


def laundry_start_timer_handler(
        user_id: int,
        callback_data: str
) -> tuple[int, datetime]:
    """
    Логика обработки кнопок "Запустить стирку" и "Запустить сушку".
    """
    settings = get_settings(user_id)

    minutes = getattr(
        settings, callback_data.replace(CallbackData.START_LAUNDRY_PREFIX, '')
    )
    start_time = datetime_now()
    end_time = start_time + timedelta(minutes=minutes)

    save_or_update_laundry(
        user_id, start_time=start_time, end_time=end_time, is_active=True
    )

    return minutes, end_time


def laundry_cancel_timer_handler(user_id: int) -> None:
    """
    Логика обработчика кнопки "Отменить таймер".
    """
    save_or_update_laundry(
        user_id, start_time=None, end_time=None, is_active=False, rings=0
    )
