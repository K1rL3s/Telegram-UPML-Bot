from io import BytesIO

from loguru import logger

from src.database.db_funcs import (
    save_or_update_class_lessons,
    save_or_update_full_lessons,
)
from src.upml.process_lessons import save_lessons
from src.utils.funcs import bytes_io_to_image_id


# изменить возвращаемые значения на (int, date)
async def load_lessons_handler(
        chat_id: int,
        image: BytesIO
) -> str:
    try:
        lessons_date, grade, full_lessons, class_lessons = save_lessons(image)
    except ValueError as e:
        logger.warning(text := f'Ошибка при загрузке расписания: {repr(e)}')
        # raise e
        return text

    lessons_id = await bytes_io_to_image_id(chat_id, full_lessons)
    class_ids = [
        await bytes_io_to_image_id(chat_id, image)
        for image in class_lessons
    ]

    save_or_update_full_lessons(lessons_id, lessons_date, grade)
    for image_id, letter in zip(class_ids, 'АБВ'):
        save_or_update_class_lessons(image_id, lessons_date, grade, letter)

    return f'{grade} {lessons_date}'
