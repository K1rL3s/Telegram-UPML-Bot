import asyncio
import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

import aiojobs
from loguru import logger


from bot.database.models.settings import Settings
from bot.database.models.users import User
from bot.upml.process_lessons import process_one_lessons_file
from bot.utils.consts import NO_DATA
from bot.utils.datehelp import format_date
from bot.utils.funcs import (
    bytes_io_to_image_id,
    name_link,
    one_notify,
    username_by_user_id,
)

if TYPE_CHECKING:
    from aiogram import Bot

    from bot.custom_types import Album
    from bot.database.repository.repository import Repository


async def process_album_lessons_func(
    chat_id: int,
    album: "Album",
    bot: "Bot",
    repo: "Repository",
) -> str:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param chat_id: Откуда пришёл альбом с расписаниями.
    :param bot: Текущий ТГ Бот.
    :param repo: Доступ к базе данных.
    :return: Склейка итогов обработки расписаний.
    """
    proccess_results: list[str | tuple[str, dt.date]] = []
    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        process_result = await process_one_lessons_func(chat_id, image, bot, repo)
        proccess_results.append(process_result)

    results: list[str] = []
    for result in proccess_results:
        if isinstance(result, tuple):
            grade, lessons_date = result
            results.append(
                f"Расписание для *{grade}-х классов* на "
                f"*{format_date(lessons_date)}* сохранено!",
            )
        else:
            results.append(result)

    return "\n".join(results)


async def process_one_lessons_func(
    chat_id: int,
    image: "BytesIO",
    bot: "Bot",
    repo: "Repository",
) -> tuple[str, "dt.date"] | str:
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param chat_id: Айди чата, откуда пришло изображение с расписанием.
    :param image: Изображение с расписанием.
    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """
    try:
        lessons_date, grade, full_lessons, class_lessons = process_one_lessons_file(
            image,
        )
    except ValueError as e:
        logger.warning(text := f"Ошибка при загрузке расписания: {repr(e)}")
        return text

    lessons_id = await bytes_io_to_image_id(chat_id, full_lessons, bot)
    class_ids = [
        await bytes_io_to_image_id(chat_id, image, bot) for image in class_lessons
    ]

    await repo.lessons.save_or_update_to_db(lessons_id, lessons_date, grade)
    for image_id, letter in zip(class_ids, "АБВ"):
        await repo.lessons.save_or_update_to_db(image_id, lessons_date, grade, letter)

    return grade, lessons_date


async def get_meal_by_date(
    repo: "Repository",
    meal: str,
    menu_date: "dt.date",
) -> str | None:
    """
    Возвращает приём пищи по названию и дате.

    :param repo: Доступ к базе данных.
    :param meal: Название приёма пищи на английском.
    :param menu_date: Дата.
    :return: Приём пищи из бд.
    """
    menu = await repo.menu.get(menu_date)
    return getattr(menu, meal, None) or NO_DATA


async def get_educators_schedule_by_date(
    repo: "Repository",
    schedule_date: "dt.date",
) -> str | None:
    """
    Возвращает расписание.

    :param repo: Доступ к базе данных.
    :param schedule_date: Дата.
    :return: Расписание воспитателей из бд.
    """
    schedule = await repo.educators.get(schedule_date)
    return getattr(schedule, "schedule", None) or NO_DATA


async def do_notifies(
    bot: "Bot",
    repo: "Repository",
    text: str,
    users: list["User"],
    from_who: int = 0,
    for_who: str = "",
) -> None:
    """
    Делатель рассылки.

    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :param text: Сообщение.
    :param users: Кому отправить сообщение.
    :param from_who: ТГ Айди отправителя (админа)
    :param for_who: Для кого рассылка.
    """
    username = await username_by_user_id(bot, from_who)
    text = (
        "🔔*Уведомление от администратора* "
        f"{name_link(username, from_who)} *{for_who}*\n\n" + text
    )

    scheduler = aiojobs.Scheduler(limit=3)
    for user in users:
        await scheduler.spawn(one_notify(bot, repo, user, text))

    while scheduler.active_count:
        await asyncio.sleep(0.5)
    await scheduler.close()


# all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
async def get_users_for_notify(
    repo: "Repository",
    notify_type: str = "",
    is_lessons: bool = False,
    is_news: bool = False,
) -> list["User"]:
    """Пользователи для рассылки по условиями.

    Преобразует notify_type из `async def notify_for_who_handler` в условия для фильтра.

    :param repo: Доступ к базе данных.
    :param notify_type: Тип уведомления из функции.
    :param is_lessons: Уведомление об изменении расписания.
    :param is_news: Уведомление о новостях (ручная рассылка).
    """
    # Если notify_type == "all", то только это условие.
    conditions = [(User.is_active, True)]

    if is_lessons:
        conditions.append((Settings.lessons_notify, True))
    if is_news:
        conditions.append((Settings.news_notify, True))

    if notify_type.startswith("grade"):
        conditions.append((Settings.grade, notify_type.split("_")[-1]))
    elif (
        len(notify_type) == 3
        and any(notify_type.startswith(grade) for grade in ("10", "11"))
        and any(notify_type.endswith(letter) for letter in "АБВ")
    ):  # XD
        conditions.append((Settings.class_, notify_type))

    return await repo.user.get_by_conditions(conditions)
