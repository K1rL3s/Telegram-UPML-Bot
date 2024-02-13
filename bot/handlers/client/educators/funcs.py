import datetime as dt

from shared.database.repository import EducatorsScheduleRepository
from shared.utils.datehelp import format_date, weekday_by_date
from shared.utils.phrases import NO_DATA


async def get_format_educators_by_date(
    repo: "EducatorsScheduleRepository",
    date: "dt.date",
) -> str:
    """Возвращает расписание воспитателей по дате.

    Н/д, если данных нет.

    :param repo: Репозиторий расписания воспитателей.
    :param date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """
    schedule = await repo.get(date)

    return (
        f"👩 <b>Воспитатели на {format_date(date)} "
        f"({weekday_by_date(date)})</b>:\n\n"
        f"{getattr(schedule, 'schedule', None) or NO_DATA}"
    )
