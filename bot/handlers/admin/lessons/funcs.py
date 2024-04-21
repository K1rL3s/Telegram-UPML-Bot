from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from bot.keyboards import (
    cancel_state_keyboard,
    choose_parallel_keyboard,
    confirm_cancel_keyboard,
)
from bot.types import Album, LessonsCollection
from shared.database.repository import ClassLessonsRepository, FullLessonsRepository
from shared.database.repository.repository import Repository
from shared.upml.album_lessons import tesseract_lessons
from shared.utils.datehelp import date_by_format, format_date, weekday_by_date
from shared.utils.funcs import multi_bytes_to_ids
from shared.utils.phrases import DONT_UNDERSTAND_DATE, SUCCESS
from shared.utils.states import EditingLessons


async def process_lessons_album_func(
    album: "Album",
    bot: "Bot",
    state: "FSMContext",
    tesseract_path: str,
) -> str:
    """
    Обработчки фотографий расписаний при нескольких штуках.

    :param album: Альбом с расписаниями.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param tesseract_path: Путь до исполняемого файла тессеракта.
    :return: Сообщение и клавиатура для пользователя.
    """
    lessons = await tesseract_lessons(bot, album, tesseract_path)
    await state.update_data(lessons=[lesson.model_dump() for lesson in lessons])

    if all(lesson.status for lesson in lessons):  # Всё успешно обработалось
        await state.set_state(EditingLessons.all_good)
        return "\n".join(lesson.text for lesson in lessons)

    await state.set_state(EditingLessons.something_bad)
    return (
        "\n".join(lesson.text for lesson in lessons if lesson.status)
        + "\n\nНе удалось распознать некоторые расписания."
        + "\nВвеcти данные вручную?"
    )


async def all_good_lessons_func(
    chat_id: int,
    bot: "Bot",
    state: "FSMContext",
    repo: "Repository",
) -> str:
    """
    Обработка кнопки "Подтвердить" при всех верных расписаниях.

    :param chat_id: Айди чата.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний уроков.
    :return: Сообщение и клавиатура для пользователя.
    """
    lessons = [
        LessonsCollection(**kwargs) for kwargs in (await state.get_data())["lessons"]
    ]

    for lesson in lessons:
        lesson.class_photo_ids = await multi_bytes_to_ids(
            chat_id,
            lesson.class_photos,
            bot,
        )
        await save_lessons_collection_to_db(
            lesson,
            repo.full_lessons,
            repo.class_lessons,
        )

    await state.clear()

    return SUCCESS


async def start_choose_grades_func(
    state: "FSMContext",
) -> tuple[str, "LessonsCollection"]:
    """
    Обработка кнопки "Подтвердить" для ручного ввода информации о расписании.

    :param state: Состояние пользователя.
    :return: Сообщение пользователю и текущее расписаний.
    """
    lessons = [
        LessonsCollection(**kwargs) for kwargs in (await state.get_data())["lessons"]
    ]

    if await state.get_state() == EditingLessons.all_good:
        for i, lesson in enumerate(lessons):
            lessons[i] = LessonsCollection(
                text=lesson.text,
                full_photo_id=lesson.full_photo_id,
            )
        await state.update_data(lessons=[lesson.model_dump() for lesson in lessons])

    await state.set_state(EditingLessons.choose_grade)

    # Начало выбора классов
    return "Для каких классов это расписание?", lessons[0]


async def choose_grades_func(
    grade: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", "LessonsCollection"]:
    """Обработчик кнопок "10 классы" и "11 классы" для нераспознанных расписаний.

    :param grade: Параллель, 10 или 11.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура пользователю.
             Если всё, то первое медиа и вводом даты.
             Если не всё, то медиа с одним изображением и выбором класса.
    """
    lessons = [
        LessonsCollection(**kwargs) for kwargs in (await state.get_data())["lessons"]
    ]
    no_grade_lessons = [lesson for lesson in lessons if lesson.grade is None]

    no_grade_lessons[0].grade = grade
    await state.update_data(lessons=[lesson.model_dump() for lesson in lessons])

    # Если есть ещё уроки без класса
    if len(no_grade_lessons) > 1:
        return (
            "Для каких классов это расписание?",
            choose_parallel_keyboard,
            no_grade_lessons[1],
        )

    # Начало ввода дат
    text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
    await state.set_state(EditingLessons.choose_date)

    return text, cancel_state_keyboard, lessons[0]


async def choose_dates_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", list["InputMediaPhoto"]]:
    """
    Обработка ввода даты для нераспознанных расписаний.

    :param text: Сообщение пользователя, дата.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура пользователю.
             Если всё, то медиа со всеми расписаниями и текстом для проверки.
             Если не всё, то медиа с одним изображением и вводом датой.
    """
    data = await state.get_data()
    lessons = [LessonsCollection(**kwargs) for kwargs in data["lessons"]]
    no_date_lessons = [lesson for lesson in lessons if lesson.date is None]

    if not (date := date_by_format(text)):
        return (
            DONT_UNDERSTAND_DATE,
            cancel_state_keyboard,
            [InputMediaPhoto(media=no_date_lessons[0].full_photo_id)],
        )

    no_date_lessons[0].date = format_date(date)
    await state.update_data(lessons=[lesson.model_dump() for lesson in lessons])

    # Если есть ещё уроки без даты
    if len(no_date_lessons) > 1:
        text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
        keyboard = cancel_state_keyboard
        media = [InputMediaPhoto(media=no_date_lessons[1].full_photo_id)]

    else:
        text = "\n".join(
            f"Расписание для <b>{good_lessons.grade}-х классов</b> "
            f"на <b>{good_lessons.date}</b> "
            f"({weekday_by_date(date_by_format(good_lessons.date))})"
            for good_lessons in lessons
        )
        keyboard = confirm_cancel_keyboard
        media = [InputMediaPhoto(media=lesson.full_photo_id) for lesson in lessons]
        await state.set_state(EditingLessons.confirm)

    return text, keyboard, media


async def confirm_edit_lessons_func(
    chat_id: int,
    bot: "Bot",
    state: "FSMContext",
    repo: "Repository",
) -> str:
    """
    Обработка подтверждения сохранения нераспознанных расписаний.

    :param chat_id: Куда отправлять фото для сохранения айдишников.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний уроков.
    :return: Сообщение пользователю.
    """
    for lesson in [
        LessonsCollection(**kwargs) for kwargs in (await state.get_data())["lessons"]
    ]:
        await repo.class_lessons.delete(
            date_by_format(lesson.date),
            lesson.grade,
        )
        lesson.class_photo_ids = await multi_bytes_to_ids(
            chat_id,
            lesson.class_photos,
            bot,
        )
        await save_lessons_collection_to_db(
            lesson,
            repo.full_lessons,
            repo.class_lessons,
        )

    await state.clear()

    return SUCCESS


async def save_lessons_collection_to_db(
    lesson: "LessonsCollection",
    full_lessons: "FullLessonsRepository",
    class_lessons: "ClassLessonsRepository",
) -> None:
    """
    Сохраняет заполненный LessonsCollection в базу данных.

    :param lesson: LessonsCollection.
    :param full_lessons: Репозиторий полных уроков.
    :param class_lessons: Репозиторий уроков для класса.
    """
    await full_lessons.save_or_update_to_db(
        lesson.full_photo_id,
        date_by_format(lesson.date),
        lesson.grade,
    )
    for photo_id, letter in zip(lesson.class_photo_ids, "АБВ"):
        await class_lessons.save_or_update_to_db(
            photo_id,
            date_by_format(lesson.date),
            lesson.grade,
            letter,
        )
