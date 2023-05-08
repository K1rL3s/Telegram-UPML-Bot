from datetime import date

from src.database.db_funcs import get_user, get_full_lessons, get_class_lessons
from src.utils.dateformat import format_date


def get_lessons_text_and_image_id(
        user_id: int,
        lesson_date: date = None
) -> tuple[str, list[str] | None]:
    """
    Возвращает сообщение с классом пользователя
    и список с двумя айдишниками картинок расписания уроков -
    для параллели и класса.

    :param user_id: Айди юзера.
    :param lesson_date: Дата расписания.
    :return: СОобщение и список с двумя айди изображения.
    """

    user = get_user(user_id)

    images = []

    if user.grade and user.letter:
        images.append(get_full_lessons(lesson_date, user.grade))
        images.append(get_class_lessons(lesson_date, user.grade, user.letter))
    else:
        images.append(get_full_lessons(lesson_date, 10))
        images.append(get_full_lessons(lesson_date, 11))

    for_grade = (f"{user.grade}{user.letter}"
                 if user.grade and user.letter
                 else "❓")

    if images[0] or images[1]:
        text = f'🛏 Расписание на *{format_date(lesson_date)}* для ' \
               f'*{for_grade}* класса.'
    else:
        images = None
        text = f'🛏 Расписание на *{format_date(lesson_date)}* для ' \
               f'*{for_grade}* класса *не найдено* :('

    return text, images
