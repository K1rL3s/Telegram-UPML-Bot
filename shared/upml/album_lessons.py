import base64
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.types import Album, LessonsCollection, LessonsProcess
from shared.upml.lessons_parser import parse_one_lessons_file
from shared.utils.datehelp import format_date, weekday_by_date

if TYPE_CHECKING:
    from aiogram import Bot


async def tesseract_lessons(
    bot: "Bot",
    album: "Album",
    tesseract_path: str,
) -> list["LessonsCollection"]:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: Текущий ТГ Бот.
    :return: Склейка итогов обработки расписаний.
    """
    results: list["LessonsCollection"] = []

    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        lessons_process = await __tesseract_one_lesson(image, tesseract_path)

        if lessons_process.grade is None or lessons_process.date is None:
            results.append(LessonsCollection(full_photo_id=photo_id))
        else:
            date, grade = lessons_process.date, lessons_process.grade
            results.append(
                LessonsCollection(
                    full_photo_id=photo_id,
                    text=(
                        f"Расписание для <b>{grade}-х классов</b> "
                        f"на <b>{format_date(date)}</b> ({weekday_by_date(date)})"
                    ),
                    status=True,
                    class_photos=[
                        base64.b64encode(lessons.read()).decode()
                        for lessons in lessons_process.class_lessons
                    ],
                    grade=grade,
                    date=format_date(date),
                ),
            )

    return results


async def __tesseract_one_lesson(
    image: "BytesIO",
    tesseract_path: str,
) -> "LessonsProcess":
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param image: Изображение с расписанием.
    :param tesseract_path: Путь до exeшника тессеракта.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """
    lessons_process = LessonsProcess()
    try:
        parse_one_lessons_file(
            lessons_process,
            image,
            tesseract_path,
        )
    except ValueError as e:
        logger.warning(f"Ошибка при обработке расписания: {repr(e)}")

    return lessons_process
