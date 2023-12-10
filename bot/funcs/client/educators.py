from typing import TYPE_CHECKING

from bot.utils.datehelp import format_date, weekday_by_date
from bot.utils.phrases import NO_DATA

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository import EducatorsScheduleRepository


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
