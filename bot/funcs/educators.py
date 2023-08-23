# @ttl_cache(ttl=60 * 60)  # Час
from datetime import date

from bot.database.repository.repository import Repository
from bot.utils.consts import NO_DATA
from bot.utils.datehelp import date_today, format_date, weekday_by_date


async def get_format_educators_by_date(
    repo: Repository, schedule_date: date = None
) -> str:
    """
    Возвращает расписание воспитателей по дате.
    Н/д, если данных нет.

    :param repo: Доступ к базе данных.
    :param schedule_date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """

    if schedule_date is None:
        schedule_date = date_today()

    schedule = await repo.educators.get_educators_schedule_by_date(schedule_date)

    return (
        f"😵 <b>Воспитатели на {format_date(schedule_date)} "
        f"({weekday_by_date(schedule_date)})</b>:\n\n"
        f"{getattr(schedule, 'schedule', None) or NO_DATA}"
    )
