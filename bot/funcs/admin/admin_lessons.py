from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from bot.keyboards import (
    cancel_state_keyboard,
    choose_grade_parallel_keyboard,
    confirm_cancel_keyboard,
    go_to_main_menu_keyboard,
)
from bot.upml.album_lessons import tesseract_album_lessons_func
from bot.utils.datehelp import date_by_format, format_date
from bot.utils.phrases import DONT_UNDERSTAND_DATE
from bot.utils.states import LoadingLessons

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext

    from bot.custom_types import Album, LessonsImage
    from bot.database.repository import LessonsRepository


async def process_lessons_album_func(
    chat_id: int,
    album: "Album",
    bot: "Bot",
    repo: "LessonsRepository",
    state: "FSMContext",
    tesseract_path: str,
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчки фотографий расписаний при нескольких штуках.

    :param chat_id: Айди чата.
    :param album: Альбом с расписаниями.
    :param bot: ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :param state: Состояние пользователя.
    :param tesseract_path: Путь до исполняемого файла тессеракта.
    :return: Сообщение и клавиатура для пользователя.
    """
    lessons = await tesseract_album_lessons_func(
        bot,
        repo,
        chat_id,
        album,
        tesseract_path,
    )

    if all(lesson.status for lesson in lessons):  # Всё успешно обработалось
        await state.clear()
        text = "\n".join(lesson.text for lesson in lessons)
        return text, go_to_main_menu_keyboard

    await state.set_state(LoadingLessons.bad_images)
    await state.update_data(lessons=[lesson for lesson in lessons if not lesson.status])

    text = (
        "\n".join(lesson.text for lesson in lessons if lesson.status)
        + "\n\nНе удалось распознать некоторые расписания.\nВвеcти данные вручную?"
    )
    return text, confirm_cancel_keyboard


async def start_choose_grades_func(
    state: "FSMContext",
) -> tuple[str, "LessonsImage"]:
    """
    Обработка кнопки "Подтвердить" для ручного ввода информации о расписании.

    :param state: Состояние пользователя.
    :return: Сообщение пользователю и текущее расписаний.
    """
    await state.set_state(LoadingLessons.choose_grade)
    data = await state.get_data()
    current_lesson = data["lessons"][0]
    await state.update_data(current_lesson=current_lesson)

    return "Для каких классов это расписание?", current_lesson


async def choose_grades_func(
    callback_data: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", "LessonsImage"]:
    """Обработчик кнопок "10 классы" и "11 классы" для нераспознанных расписаний.

    :param callback_data: Сообщение пользователя, дата.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура пользователю.
             Если всё, то первое медиа и вводом даты.
             Если не всё, то медиа с одним изображением и выбором класса.
    """
    data = await state.get_data()
    lessons: list[LessonsImage] = data["lessons"]
    current_lesson: LessonsImage = data["current_lesson"]

    current_lesson.grade = callback_data.split("_")[-1]

    if no_grade_lessons := [lesson for lesson in lessons if lesson.grade is None]:
        current_lesson = no_grade_lessons[0]
        text = "Для каких классов это расписание?"
        keyboard = choose_grade_parallel_keyboard
    else:
        current_lesson = data["lessons"][0]
        text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
        keyboard = cancel_state_keyboard
        await state.set_state(LoadingLessons.choose_date)

    await state.update_data(current_lesson=current_lesson)

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
    lessons: list[LessonsImage] = data["lessons"]
    current_lesson: LessonsImage = data["current_lesson"]

    end = False
    if date := date_by_format(text):
        current_lesson.date = date

        if no_date_lessons := [lesson for lesson in lessons if lesson.date is None]:
            current_lesson = no_date_lessons[0]
            text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
            await state.update_data(current_lesson=current_lesson)
        else:
            end = True
            text = "\n".join(
                f"Расписание для <b>{good_lessons.grade}-х классов</b> "
                f"на <b>{format_date(good_lessons.date)}</b>"
                for good_lessons in lessons
            )
            await state.set_state(LoadingLessons.confirm)
    else:
        text = DONT_UNDERSTAND_DATE

    if end:
        media = [InputMediaPhoto(media=lesson.photo_id) for lesson in lessons]
        keyboard = confirm_cancel_keyboard
    else:
        media = [InputMediaPhoto(media=current_lesson.photo_id)]
        keyboard = cancel_state_keyboard

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
        lesson: LessonsImage
        await repo.delete_class_lessons(
            lesson.date,
            lesson.grade,
        )
        await repo.save_prepared_to_db(
            lesson,
            [],
        )

    await state.clear()

    return "Успешно!"
