import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.custom_types import Album, LessonsImage
from bot.upml.pillow_lessons import process_one_lessons_file
from bot.utils.datehelp import format_date
from bot.utils.funcs import bytes_io_to_image_id

if TYPE_CHECKING:
    from aiogram import Bot

    from bot.database.repository import LessonsRepository


async def tesseract_album_lessons_func(
    bot: "Bot",
    repo: "LessonsRepository",
    chat_id: int,
    album: "Album",
    tesseract_path: str,
) -> list[LessonsImage]:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param chat_id: Откуда пришёл альбом с расписаниями.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: Текущий ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :return: Склейка итогов обработки расписаний.
    """
    results: list[LessonsImage] = []

    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        result = await _tesseract_one_lessons_func(
            bot,
            repo,
            chat_id,
            image,
            tesseract_path,
        )

        if isinstance(result, tuple):
            grade, date = result
            results.append(
                LessonsImage(
                    text=(
                        f"Расписание для <b>{grade}-х классов</b> "
                        f"на <b>{format_date(date)}</b> сохранено!"
                    ),
                    status=True,
                    photo_id=photo_id,
                    grade=grade,
                    date=date,
                ),
            )
        else:
            results.append(
                LessonsImage(
                    text=result,
                    status=False,
                    photo_id=photo_id,
                    grade=None,
                    date=None,
                ),
            )

    return results


async def _tesseract_one_lessons_func(
    bot: "Bot",
    repo: "LessonsRepository",
    chat_id: int,
    image: "BytesIO",
    tesseract_path: str,
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

    full_lessons_id = await bytes_io_to_image_id(chat_id, full_lessons, bot)
    class_lessons_ids = [
        await bytes_io_to_image_id(chat_id, class_image, bot)
        for class_image in class_lessons
    ]

    await repo.save_prepared_to_db(
        LessonsImage(
            text=None,
            status=True,
            photo_id=full_lessons_id,
            grade=grade,
            date=date,
        ),
        [
            LessonsImage(
                text=None,
                status=True,
                photo_id=class_id,
                grade=grade,
                date=date,
            )
            for class_id in class_lessons_ids
        ],
    )

    return grade, date
