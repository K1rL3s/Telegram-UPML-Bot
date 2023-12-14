from typing import TYPE_CHECKING

from aiogram.types import InputMediaPhoto

from bot.keyboards import lessons_keyboard
from shared.utils.datehelp import format_date, weekday_by_date
from shared.utils.phrases import QUESTION

if TYPE_CHECKING:
    import datetime as dt

    from aiogram import Bot

    from shared.database.repository.repository import Repository


async def send_lessons_images(
    user_id: int,
    chat_id: int,
    date: "dt.date",
    bot: "Bot",
    repo: "Repository",
) -> str | None:
    """
    Общий код обработчиков просмотра уроков. Если имеется, отправляет фото расписания.

    Отправляет расписание уроков паралелли и класса, если выбран класс.
    Отправляет расписание двух паралеллей, если не выбран класс.

    :param user_id: ТГ Айди.
    :param chat_id: Айди чата с пользователем.
    :param date: Дата уроков.
    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :return: Сообщение для пользователя.
    """
    text, images = await get_lessons_for_user(user_id, date, repo)

    if any(images):
        messages = await bot.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=media_id) for media_id in images if media_id],
        )
        await messages[0].reply(text=text, reply_markup=lessons_keyboard(date))
        return

    return text


async def get_lessons_for_user(
    user_id: int,
    date: "dt.date",
    repo: "Repository",
) -> tuple[str, list[str | None]]:
    """Возвращает сообщение о расписании уроков и айдишники фото.

    Если класс выбран, то список из двух айди с расписанием паралелли и класса.
    Если класс не выбран, то список из двух айди с расписаниями параллелей.
    Если расписаний нет, то None.

    :param user_id: Айди юзера.
    :param date: Дата расписания.
    :param repo: Доступ к базе данных.
    :return: Сообщение и список с двумя айди изображений.
    """
    settings = await repo.settings.get(user_id)

    if settings.class_:
        full_lessons = await repo.full_lessons.get(date, settings.grade)
        class_lessons = await repo.class_lessons.get(date, settings.class_)
        images = [
            getattr(full_lessons, "file_id", None),
            getattr(class_lessons, "file_id", None),
        ]
    else:
        full_10_lessons = await repo.full_lessons.get(date, "10")
        full_11_lessons = await repo.full_lessons.get(date, "11")
        images = [
            getattr(full_10_lessons, "file_id", None),
            getattr(full_11_lessons, "file_id", None),
        ]

    for_class = settings.class_ if settings.class_ else QUESTION
    if any(images):
        text = (
            f"✏ Расписание на <b>{format_date(date)}</b> ({weekday_by_date(date)}) "
            f"для <b>{for_class}</b> класса."
        )
    else:
        text = (
            f"💤 Расписание на <b>{format_date(date)}</b> ({weekday_by_date(date)}) "
            f"для <b>{for_class}</b> класса не найдено :("
        )

    return text, images
