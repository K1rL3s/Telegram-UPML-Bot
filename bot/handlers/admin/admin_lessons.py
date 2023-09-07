from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import InputMediaPhoto

from bot.custom_types import Album, LessonsImage
from bot.filters import IsAdmin
from bot.funcs.admin.admin_lessons import (
    save_lessons_to_db_func,
    tesseract_album_lessons_func,
)
from bot.keyboards import (
    cancel_state_keyboard,
    confirm_cancel_keyboard,
    go_to_main_menu_keyboard,
)
from bot.keyboards.admin.admin_lessons import choose_grade_parallel_keyboard
from bot.utils.datehelp import date_by_format, format_date
from bot.utils.enums import AdminCallback
from bot.utils.states import LoadingLessons

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.settings import Settings
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == AdminCallback.UPLOAD_LESSONS, IsAdmin())
async def start_process_lessons_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Загрузить уроки"."""
    await state.set_state(LoadingLessons.image)
    text = "Отправьте изображение(-я) расписания уроков"

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(
    StateFilter(LoadingLessons.image),
    ~F.media_group_id,
    F.content_type.in_({"photo"}),
    IsAdmin(),
)
async def process_lessons_handler(
    message: "Message",
    state: "FSMContext",
    settings: "Settings",
    repo: "Repository",
) -> None:
    """Обработчки фотографий расписаний при только одной штуке."""
    album = Album.model_validate(
        {
            "photo": [message.photo[-1]],
            "messages": [message],
            "caption": message.html_text,
        },
        context={"bot": message.bot},
    )
    await process_lessons_album_handler(message, state, settings, repo, album)


@router.message(
    StateFilter(LoadingLessons.image),
    F.media_group_id,
    F.content_type.in_({"photo"}),
    IsAdmin(),
)
async def process_lessons_album_handler(
    message: "Message",
    state: "FSMContext",
    settings: "Settings",
    repo: "Repository",
    album: "Album",
) -> None:
    """Обработчки фотографий расписаний при нескольких штуках."""
    lessons = await tesseract_album_lessons_func(
        message.bot,
        repo.lessons,
        message.chat.id,
        album,
        settings.other.TESSERACT_PATH,
    )

    if all(lesson.status for lesson in lessons):  # Всё успешно обработалось
        await state.clear()
        text = "\n".join(lesson.text for lesson in lessons)
        await message.reply(text=text, reply_markup=go_to_main_menu_keyboard)
        return

    await state.set_state(LoadingLessons.bad_images)
    await state.update_data(lessons=[lesson for lesson in lessons if not lesson.status])

    text = (
        "\n".join(lesson.text for lesson in lessons if lesson.status)
        + "\n\nНе удалось распознать некоторые расписания.\nВвеcти данные вручную?"
    )
    await message.reply(
        text=text,
        reply_markup=confirm_cancel_keyboard,
    )


@router.callback_query(
    StateFilter(LoadingLessons.bad_images),
    F.data == AdminCallback.CONFIRM,
    IsAdmin(),
)
async def start_choose_grades_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработка кнопки "Подтвердить" для ручного ввода информации о расписании."""
    await state.set_state(LoadingLessons.choose_grade)
    data = await state.get_data()
    current_lessons = data["lessons"][0]
    await state.update_data(current_lessons=current_lessons)

    photo = await callback.bot.send_media_group(
        chat_id=callback.message.chat.id,
        media=[InputMediaPhoto(media=current_lessons.photo_id)],
    )
    await photo[0].reply(
        text="Для каких классов это расписание?",
        reply_markup=choose_grade_parallel_keyboard,
    )


@router.callback_query(
    StateFilter(LoadingLessons.choose_grade),
    F.data.in_(
        {
            AdminCallback.UPLOAD_LESSONS_FOR_10,
            AdminCallback.UPLOAD_LESSONS_FOR_11,
        },
    ),
    IsAdmin(),
)
async def choose_grades_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок "10 классы" и "11 классы" для нераспознанных расписаний."""
    data = await state.get_data()
    lessons: list[LessonsImage] = data["lessons"]
    current_lessons: LessonsImage = data["current_lessons"]

    current_lessons.grade = callback.data.split("_")[-1]

    if no_grade_lessons := [lesson for lesson in lessons if lesson.grade is None]:
        current_lessons = no_grade_lessons[0]
        text = "Для каких классов это расписание?"
        keyboard = choose_grade_parallel_keyboard
    else:
        current_lessons = data["lessons"][0]
        text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
        keyboard = cancel_state_keyboard
        await state.set_state(LoadingLessons.choose_date)

    await state.update_data(current_lessons=current_lessons)
    photo = await callback.bot.send_media_group(
        chat_id=callback.message.chat.id,
        media=[InputMediaPhoto(media=current_lessons.photo_id)],
    )
    await photo[0].reply(
        text=text,
        reply_markup=keyboard,
    )


@router.message(StateFilter(LoadingLessons.choose_date), IsAdmin())
async def choose_dates_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработка ввода даты для нераспознанных расписаний."""
    data = await state.get_data()
    lessons: list[LessonsImage] = data["lessons"]
    current_lessons: LessonsImage = data["current_lessons"]

    end = False
    if date := date_by_format(message.text):
        current_lessons.date = date

        if no_date_lessons := [lesson for lesson in lessons if lesson.date is None]:
            current_lessons = no_date_lessons[0]
            text = "Введите дату расписания в формате <b>ДД.ММ.ГГГГ</b>"
            await state.update_data(current_lessons=current_lessons)
        else:
            end = True
            text = "\n".join(
                f"Расписание для <b>{good_lessons.grade}-х классов</b> "
                f"на <b>{format_date(good_lessons.date)}</b>"
                for good_lessons in lessons
            )
            await state.set_state(LoadingLessons.confirm)
    else:
        text = "❌ Не понял это как дату, попробуйте ещё раз."

    if end:
        media = [InputMediaPhoto(media=lesson.photo_id) for lesson in lessons]
        keyboard = confirm_cancel_keyboard
    else:
        media = [InputMediaPhoto(media=current_lessons.photo_id)]
        keyboard = cancel_state_keyboard

    photo = await message.bot.send_media_group(
        chat_id=message.chat.id,
        media=media,
    )
    await photo[0].reply(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    StateFilter(LoadingLessons.confirm),
    F.data == AdminCallback.CONFIRM,
)
async def confirm_edit_lessons_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработка подтверждения сохранения нераспознанных расписаний."""
    data = await state.get_data()

    for lesson in data["lessons"]:
        lesson: LessonsImage
        await save_lessons_to_db_func(
            repo.lessons,
            lesson,
            [],
        )

    await state.clear()

    await callback.message.answer(
        text="Успешно!",
        reply_markup=go_to_main_menu_keyboard,
    )
