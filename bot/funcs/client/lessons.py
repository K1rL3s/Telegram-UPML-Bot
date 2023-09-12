from typing import TYPE_CHECKING

from bot.utils.datehelp import format_date, weekday_by_date
from bot.utils.phrases import QUESTION


if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository import LessonsRepository, SettingsRepository


async def get_lessons_for_user(
    settings_repo: "SettingsRepository",
    lessons_repo: "LessonsRepository",
    user_id: int,
    date: "dt.date" = None,
) -> tuple[str, list[str | None]]:
    """Возвращает сообщение о расписании уроков и айдишники фото.

    Если класс выбран, то список из двух айди с расписанием паралелли и класса.
    Если класс не выбран, то список из двух айди с расписаниями параллелей.
    Если расписаний нет, то None.

    :param settings_repo: Репозиторий настроек.
    :param lessons_repo: Репозиторий расписаний уроков.
    :param user_id: Айди юзера.
    :param date: Дата расписания.
    :return: Сообщение и список с двумя айди изображений.
    """
    settings = await settings_repo.get(user_id)

    if settings.class_:
        full_lessons = await lessons_repo.get(date, settings.grade)
        class_lessons = await lessons_repo.get(date, settings.class_)  # noqa
        images = [
            getattr(full_lessons, "image", None),
            getattr(class_lessons, "image", None),
        ]
    else:
        full_10_lessons = await lessons_repo.get(date, "10")
        full_11_lessons = await lessons_repo.get(date, "11")
        images = [
            getattr(full_10_lessons, "image", None),
            getattr(full_11_lessons, "image", None),
        ]

    for_class = settings.class_ if settings.class_ else QUESTION
    if any(images):
        text = (
            f"✏ Расписание на <b>{format_date(date)}</b> ({weekday_by_date(date)}) "
            f"для <b>{for_class}</b> класса."
        )
    else:
        text = (
            f"🛏 Расписание на <b>{format_date(date)}</b> ({weekday_by_date(date)}) "
            f"для <b>{for_class}</b> класса не найдено :(."
        )

    return text, images
