import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.custom_types import Album, LessonsAlbum
from bot.upml.pillow_lessons import parse_one_lessons_file
from bot.utils.datehelp import format_date, weekday_by_date


if TYPE_CHECKING:
    from aiogram import Bot


async def tesseract_album_lessons_func(
    bot: "Bot",
    album: "Album",
    tesseract_path: str,
) -> list["LessonsAlbum"]:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: Текущий ТГ Бот.
    :return: Склейка итогов обработки расписаний.
    """
    results: list["LessonsAlbum"] = []

    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        result = await _tesseract_one_lessons_func(image, tesseract_path)

        if isinstance(result, str):
            results.append(
                LessonsAlbum(
                    full_photo_id=photo_id,
                    text=result,
                ),
            )
        else:
            grade, date, class_lessons = result
            results.append(
                LessonsAlbum(
                    full_photo_id=photo_id,
                    text=(
                        f"Расписание для <b>{grade}-х классов</b> "
                        f"на <b>{format_date(date)}</b> ({weekday_by_date(date)})"
                    ),
                    status=True,
                    class_photos=class_lessons,
                    grade=grade,
                    date=date,
                ),
            )

    return results


async def _tesseract_one_lessons_func(
    image: "BytesIO",
    tesseract_path: str,
) -> tuple[str, "dt.date", list["BytesIO"]] | str:
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param image: Изображение с расписанием.
    :param tesseract_path: Путь до exeшника тессеракта.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """
    try:
        return parse_one_lessons_file(
            image,
            tesseract_path,
        )
    except ValueError as e:
        logger.warning(text := f"Ошибка при загрузке расписания: {repr(e)}")
        return text