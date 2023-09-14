import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.custom_types import Album, LessonsAlbum
from bot.upml.pillow_lessons import parse_one_lessons_file
from bot.utils.datehelp import format_date
from bot.utils.funcs import bytes_io_to_image_id

if TYPE_CHECKING:
    from aiogram import Bot


async def tesseract_album_lessons_func(
    chat_id: int,
    bot: "Bot",
    album: "Album",
    tesseract_path: str,
) -> list["LessonsAlbum"]:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param chat_id: Откуда пришёл альбом с расписаниями.
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

        if isinstance(result, tuple):
            grade, date, class_lessons = result
            class_lessons = await _prepare_class_lessons(
                chat_id,
                class_lessons,
                bot,
            )
            results.append(
                LessonsAlbum(
                    text=(
                        f"Расписание для <b>{grade}-х классов</b> "
                        f"на <b>{format_date(date)}</b>"
                    ),
                    status=True,
                    full_photo_id=photo_id,
                    class_photo_ids=class_lessons,
                    grade=grade,
                    date=date,
                ),
            )
        else:
            results.append(
                LessonsAlbum(
                    text=result,
                    status=False,
                    full_photo_id=photo_id,
                    class_photo_ids=[],
                    grade=None,
                    date=None,
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


async def _prepare_class_lessons(
    chat_id: int,
    class_lessons: list["BytesIO"],
    bot: "Bot",
) -> list[str]:
    """
    Перевод изображений из байтов в айдишники файлов телеграма.

    :param chat_id: Куда отправлять для сохранения.
    :param class_lessons: Файлы с расписаниями по классам.
    :param bot: ТГ Бот.
    :return: Айдишник полного расписания и айдишники отдельных расписаний.
    """
    return [
        await bytes_io_to_image_id(chat_id, class_image, bot)
        for class_image in class_lessons
    ]
