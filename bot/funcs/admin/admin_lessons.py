from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from bot.custom_types import LessonsAlbum
from bot.keyboards import (
    cancel_state_keyboard,
    choose_grade_parallel_keyboard,
    confirm_cancel_keyboard,
    go_to_main_menu_keyboard,
)
from bot.keyboards.admin.admin import confirm_unconfirm_keyboard
from bot.upml.album_lessons import tesseract_album_lessons_func
from bot.utils.datehelp import date_by_format, format_date, weekday_by_date
from bot.utils.funcs import multi_bytes_to_ids
from bot.utils.phrases import DONT_UNDERSTAND_DATE
from bot.utils.states import LoadingLessons

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext

    from bot.custom_types import Album
    from bot.database.repository import LessonsRepository


async def process_lessons_album_func(
    album: "Album",
    bot: "Bot",
    state: "FSMContext",
    tesseract_path: str,
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчки фотографий расписаний при нескольких штуках.

    :param album: Альбом с расписаниями.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param tesseract_path: Путь до исполняемого файла тессеракта.
    :return: Сообщение и клавиатура для пользователя.
    """
    lessons = await tesseract_album_lessons_func(bot, album, tesseract_path)
    await state.update_data(lessons=lessons)

    if all(lesson.status for lesson in lessons):  # Всё успешно обработалось
        await state.set_state(LoadingLessons.all_good)
        return "\n".join(lesson.text for lesson in lessons), confirm_unconfirm_keyboard

    await state.set_state(LoadingLessons.something_bad)
    text = (
        "\n".join(lesson.text for lesson in lessons if lesson.status)
        + "\n\nНе удалось распознать некоторые расписания.\nВвеcти данные вручную?"
    )
    return text, confirm_cancel_keyboard


async def all_good_lessons_func(
    chat_id: int,
    bot: "Bot",
    state: "FSMContext",
    repo: "LessonsRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработка кнопки "Подтвердить" при всех верных расписаниях.

    :param chat_id: Айди чата.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний уроков.
    :return: Сообщение и клавиатура для пользователя.
    """
    lessons: list["LessonsAlbum"] = (await state.get_data())["lessons"]

    for lesson in lessons:
        lesson.class_photo_ids = await multi_bytes_to_ids(
            chat_id,
            lesson.class_photos,
            bot,
        )
        await repo.save_prepared_to_db(lesson)

    await state.clear()

    return "Успешно!", go_to_main_menu_keyboard


async def start_choose_grades_func(
    state: "FSMContext",
) -> tuple[str, "LessonsAlbum"]:
    """
    Обработка кнопки "Подтвердить" для ручного ввода информации о расписании.

    :param state: Состояние пользователя.
    :return: Сообщение пользователю и текущее расписаний.
    """
    data = await state.get_data()
    lessons: list["LessonsAlbum"] = data["lessons"]

    if await state.get_state() == LoadingLessons.all_good:
        for i, lesson in enumerate(lessons):
            lessons[i] = LessonsAlbum(
                text=lesson.text,
                full_photo_id=lesson.full_photo_id,
            )
        await state.update_data(lessons=lessons)

    current_lesson = lessons[0]
    await state.update_data(current_lesson=current_lesson)
    await state.set_state(LoadingLessons.choose_grade)

    # Начало выбора классов
    return "Для каких классов это расписание?", current_lesson


async def choose_grades_func(
    callback_data: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", "LessonsAlbum"]:
    """Обработчик кнопок "10 классы" и "11 классы" для нераспознанных расписаний.

    :param callback_data: Сообщение пользователя, дата.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура пользователю.
             Если всё, то первое медиа и вводом даты.
             Если не всё, то медиа с одним изображением и выбором класса.
    """
    data = await state.get_data()
    lessons: list[LessonsAlbum] = data["lessons"]
    current_lesson: LessonsAlbum = data["current_lesson"]

    current_lesson.grade = callback_data.split("_")[-1]

    if no_grade_lessons := [lesson for lesson in lessons if lesson.grade is None]:
        current_lesson = no_grade_lessons[0]
        await state.update_data(current_lesson=current_lesson)
        return (
            "Для каких классов это расписание?",
            choose_grade_parallel_keyboard,
            current_lesson,
        )

    # Начало ввода дат
    current_lesson = data["lessons"][0]
    await state.update_data(current_lesson=current_lesson)

    text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
    keyboard = cancel_state_keyboard
    await state.set_state(LoadingLessons.choose_date)

    return text, keyboard, current_lesson


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
    lessons: list[LessonsAlbum] = data["lessons"]
    current_lesson: LessonsAlbum = data["current_lesson"]

    if not (date := date_by_format(text)):
        return (
            DONT_UNDERSTAND_DATE,
            cancel_state_keyboard,
            [InputMediaPhoto(media=current_lesson.full_photo_id)],
        )

    current_lesson.date = date

    if no_date_lessons := [lesson for lesson in lessons if lesson.date is None]:
        current_lesson = no_date_lessons[0]

        text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
        keyboard = cancel_state_keyboard
        media = [InputMediaPhoto(media=current_lesson.full_photo_id)]
        await state.update_data(current_lesson=current_lesson)

    else:
        text = "\n".join(
            f"Расписание для <b>{good_lessons.grade}-х классов</b> "
            f"на <b>{format_date(good_lessons.date)}</b> "
            f"({weekday_by_date(good_lessons.date)})"
            for good_lessons in lessons
        )
        keyboard = confirm_cancel_keyboard
        media = [InputMediaPhoto(media=lesson.full_photo_id) for lesson in lessons]
        await state.set_state(LoadingLessons.confirm)

    return text, keyboard, media


async def confirm_edit_lessons_func(
    state: "FSMContext",
    repo: "LessonsRepository",
) -> str:
    """
    Обработка подтверждения сохранения нераспознанных расписаний.

    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний уроков.
    :return: Сообщение пользователю.
    """
    data = await state.get_data()

    for lesson in data["lessons"]:
        lesson: LessonsAlbum
        await repo.delete_class_lessons(
            lesson.date,
            lesson.grade,
        )
        await repo.save_prepared_to_db(lesson)

    await state.clear()

    return "Успешно!"
