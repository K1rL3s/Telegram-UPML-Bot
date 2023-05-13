from datetime import date

from src.database.db_funcs import get_user, get_full_lessons, get_class_lessons
from src.utils.datehelp import format_date


def get_lessons_text_and_image_id(
        user_id: int,
        lesson_date: date = None
) -> tuple[str, list[str] | None]:
    """
    Возвращает сообщение для пользователя и:
    Если класс выбран, то список из двух
        айди с расписанием паралелли и выбранного класса.
    Если класс не выбран, то список из двух
        айди с расписаниями параллелей.
    Если расписаний нет, то None.

    :param user_id: Айди юзера.
    :param lesson_date: Дата расписания.
    :return: Сообщение и список с двумя айди изображений.
    """

    user = get_user(user_id)

    images = []

    if user.class_:
        images.append(get_full_lessons(lesson_date, user.grade))
        images.append(get_class_lessons(lesson_date, user.class_))
    else:
        images.append(get_full_lessons(lesson_date, "10"))
        images.append(get_full_lessons(lesson_date, "11"))

    for_class = user.class_ if user.class_ else "❓"

    if images[0] or images[1]:
        text = f'🛏 Расписание на *{format_date(lesson_date)}* для ' \
               f'*{for_class}* класса.'
    else:
        images = None
        text = f'🛏 Расписание на *{format_date(lesson_date)}* для ' \
               f'*{for_class}* класса *не найдено* :('

    return text, images
