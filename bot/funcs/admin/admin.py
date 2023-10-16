from typing import TYPE_CHECKING

from bot.database.models.settings import Settings
from bot.database.models.users import User
from bot.utils.phrases import NO_DATA

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository import (
        EducatorsScheduleRepository,
        MenuRepository,
        UserRepository,
    )


async def get_meal_by_date(
    repo: "MenuRepository",
    meal: str,
    date: "dt.date",
) -> str | None:
    """
    Возвращает приём пищи по названию и дате.

    :param repo: Репозиторий расписаний столовой.
    :param meal: Название приёма пищи на английском.
    :param date: Дата.
    :return: Приём пищи из бд.
    """
    menu = await repo.get(date)
    return getattr(menu, meal, None) or NO_DATA


async def get_educators_schedule_by_date(
    repo: "EducatorsScheduleRepository",
    date: "dt.date",
) -> str | None:
    """
    Возвращает расписание воспитателей по дате.

    :param repo: Репозиторий расписаний воспитателей.
    :param date: Дата.
    :return: Расписание воспитателей из бд.
    """
    schedule = await repo.get(date)
    return getattr(schedule, "schedule", None) or NO_DATA


async def get_users_for_notify(
    repo: "UserRepository",
    for_who: str,  # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
    is_lessons: bool = False,
    is_news: bool = False,
) -> list["User"]:
    """Пользователи для рассылки по условиями.

    Преобразует notify_type из `async def notify_for_who_handler` в условия для фильтра.

    :param repo: Репозиторий пользователей.
    :param for_who: Кому уведомление.
    :param is_lessons: Уведомление об изменении расписания.
    :param is_news: Уведомление о новостях (ручная рассылка).
    """
    conditions = [(User.is_active, True)]

    if is_lessons:
        conditions.append((Settings.lessons_notify, True))
    if is_news:
        conditions.append((Settings.news_notify, True))

    if for_who.startswith("grade"):
        conditions.append((Settings.grade, for_who.split("_")[-1]))
    elif (
        len(for_who) == 3
        and any(for_who.startswith(grade) for grade in ("10", "11"))
        and any(for_who.endswith(letter) for letter in "АБВ")
    ):  # XD
        conditions.append((Settings.class_, for_who))

    return await repo.get_by_conditions(conditions)
