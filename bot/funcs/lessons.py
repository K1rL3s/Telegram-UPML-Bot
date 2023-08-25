from typing import TYPE_CHECKING

from bot.utils.datehelp import format_date, weekday_by_date

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository.repository import Repository


async def get_lessons_for_user(
    repo: "Repository",
    user_id: int,
    lesson_date: "dt.date" = None,
) -> tuple[str, list[str | None]]:
    """Возвращает сообщение о расписании уроков и айдишники фото.

    Если класс выбран, то список из двух айди с расписанием паралелли и класса.
    Если класс не выбран, то список из двух айди с расписаниями параллелей.
    Если расписаний нет, то None.

    :param repo: Доступ к базе данных.
    :param user_id: Айди юзера.
    :param lesson_date: Дата расписания.
    :return: Сообщение и список с двумя айди изображений.
    """
    settings = await repo.settings.get(user_id)

    if settings.class_:
        full_lessons = await repo.lessons.get(lesson_date, settings.grade)
        class_lessons = await repo.lessons.get(lesson_date, settings.class_)
        images = [
            getattr(full_lessons, "image", None),
            getattr(class_lessons, "image", None),
        ]
    else:
        full_10_lessons = await repo.lessons.get(lesson_date, "10")
        full_11_lessons = await repo.lessons.get(lesson_date, "11")
        images = [
            getattr(full_10_lessons, "image", None),
            getattr(full_11_lessons, "image", None),
        ]

    for_class = settings.class_ if settings.class_ else "❓"

    if any(images):
        text = (
            f"✏ Расписание на *{format_date(lesson_date)}* "
            f"({weekday_by_date(lesson_date)}) для *{for_class}* класса."
        )
    else:
        text = (
            f"🛏 Расписание на *{format_date(lesson_date)}* "
            f"({weekday_by_date(lesson_date)}) "
            f"для *{for_class}* класса не найдено :(."
        )

    return text, images
