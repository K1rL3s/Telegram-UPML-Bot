import asyncio
from datetime import date
from io import BytesIO

import aiojobs
from aiogram import Bot
from loguru import logger

from src.database.db_funcs import (
    get_menu_by_date, get_users_by_conditions, save_or_update_lessons,
)
from src.database.models.users import User
from src.upml.process_lessons import save_lessons
from src.utils.funcs import (
    one_notify, bytes_io_to_image_id, tg_click_name,
    username_by_user_id,
)


async def load_lessons_handler(
        chat_id: int,
        image: BytesIO,
        bot: Bot,
) -> tuple[str, date] | str:
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param chat_id: Айди чата, откуда пришло изображение с расписанием.
    :param image: Изображение с расписанием.
    :param bot: ТГ Бот.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """

    try:
        lessons_date, grade, full_lessons, class_lessons = save_lessons(image)
    except ValueError as e:
        logger.warning(text := f'Ошибка при загрузке расписания: {repr(e)}')
        # raise e
        return text

    lessons_id = await bytes_io_to_image_id(chat_id, full_lessons, bot)
    class_ids = [
        await bytes_io_to_image_id(chat_id, image, bot)
        for image in class_lessons
    ]

    await save_or_update_lessons(lessons_id, lessons_date, grade)
    for image_id, letter in zip(class_ids, 'АБВ'):
        await save_or_update_lessons(image_id, lessons_date, grade, letter)

    return grade, lessons_date


async def get_meal_by_date(meal: str, menu_date: date) -> str | None:
    """
    Возвращает приём пищи по названию и дате.

    :param meal: Название приёма пищи на английском.
    :param menu_date: Дата.
    :return: Приём пищи из бд.
    """
    menu = await get_menu_by_date(menu_date)
    return getattr(menu, meal, None)


async def do_notifies(
        bot: Bot,
        text: str,
        users: list[User],
        from_who: int = 0,
        for_who: str = ''
) -> None:
    """
    Делатель рассылки.

    :param bot: ТГ Бот.
    :param text: Сообщение.
    :param users: Кому отправить сообщение.
    :param from_who: ТГ Айди отправителя (админа)
    :param for_who: Для кого рассылка.
    """

    username = await username_by_user_id(bot, from_who)
    text = '🔔*Уведомление от администратора* ' \
           f'{tg_click_name(username, from_who)} *{for_who}*\n\n' + text

    scheduler = aiojobs.Scheduler(limit=3)
    for user in users:
        await scheduler.spawn(one_notify(text, user, bot))

    while scheduler.active_count:
        await asyncio.sleep(0.5)
    await scheduler.close()


# all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
async def get_users_for_notify(
        notify_type: str = '',
        is_lessons: bool = False,
        is_news: bool = False,
) -> list[User]:
    """
    Преобразование notify_type
    из src/view/admin/admin_notifies.py ``async def notify_for_who_view``
    в условия для фильтра.

    :param notify_type: Тип уведомления из функции.
    :param is_lessons: Уведомление об изменении расписания.
    :param is_news: Уведомление о новостях (ручная рассылка).
    """

    conditions = [('is_active', True)]

    if is_lessons:
        conditions.append(('lessons_notify', True))
    if is_news:
        conditions.append(('news_notify', True))

    if notify_type.startswith('grade'):
        conditions.append(('grade', notify_type.split('_')[-1]))
    elif len(notify_type) == 3 \
            and any(notify_type.startswith(grade) for grade in ('10', '11')) \
            and any(notify_type.endswith(letter) for letter in 'АБВ'):  # XD
        conditions.append(('class_', notify_type))

    return await get_users_by_conditions(conditions)
