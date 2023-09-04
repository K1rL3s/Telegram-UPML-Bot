from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.database.models.settings import Settings
from bot.database.models.users import User
from bot.upml.process_lessons import process_one_lessons_file
from bot.utils.consts import NO_DATA
from bot.utils.datehelp import format_date
from bot.utils.funcs import bytes_io_to_image_id

if TYPE_CHECKING:
    import datetime as dt

    from aiogram import Bot

    from bot.custom_types import Album
    from bot.database.repository import (
        EducatorsScheduleRepository,
        LessonsRepository,
        MenuRepository,
        UserRepository,
    )


async def process_album_lessons_func(
    chat_id: int,
    album: "Album",
    tesseract_path: str,
    bot: "Bot",
    repo: "LessonsRepository",
) -> str:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param chat_id: Откуда пришёл альбом с расписаниями.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: Текущий ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :return: Склейка итогов обработки расписаний.
    """
    save_results: list[str | tuple[str, dt.date]] = []
    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        save_result = await save_one_lessons_to_db(
            chat_id,
            image,
            tesseract_path,
            bot,
            repo,
        )
        save_results.append(save_result)

    results: list[str] = []
    for result in save_results:
        if isinstance(result, tuple):
            grade, lessons_date = result
            results.append(
                f"Расписание для *{grade}-х классов* на "
                f"*{format_date(lessons_date)}* сохранено!",
            )
        else:
            results.append(result)

    return "\n".join(results)


async def save_one_lessons_to_db(
    chat_id: int,
    image: "BytesIO",
    tesseract_path: str,
    bot: "Bot",
    repo: "LessonsRepository",
) -> tuple[str, "dt.date"] | str:
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param chat_id: Айди чата, откуда пришло изображение с расписанием.
    :param image: Изображение с расписанием.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """
    try:
        date, grade, full_lessons, class_lessons = process_one_lessons_file(
            image,
            tesseract_path,
        )
    except ValueError as e:
        logger.warning(text := f"Ошибка при загрузке расписания: {repr(e)}")
        return text

    lessons_id = await bytes_io_to_image_id(chat_id, full_lessons, bot)
    images_ids = [
        await bytes_io_to_image_id(chat_id, image, bot) for image in class_lessons
    ]

    await repo.save_or_update_to_db(lessons_id, date, grade)
    for image_id, letter in zip(images_ids, "АБВ"):
        await repo.save_or_update_to_db(image_id, date, grade, letter)

    return grade, date


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
    notify_type: str,  # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
    is_lessons: bool = False,
    is_news: bool = False,
) -> list["User"]:
    """Пользователи для рассылки по условиями.

    Преобразует notify_type из `async def notify_for_who_handler` в условия для фильтра.

    :param repo: Репозиторий пользователей.
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

    return await repo.get_by_conditions(conditions)
