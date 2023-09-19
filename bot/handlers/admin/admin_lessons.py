from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import InputMediaPhoto

from bot.custom_types import Album
from bot.funcs.admin.admin_lessons import (
    all_good_lessons_func,
    choose_dates_func,
    choose_grades_func,
    confirm_edit_lessons_func,
    process_lessons_album_func,
    start_choose_grades_func,
)
from bot.keyboards import (
    cancel_state_keyboard,
    go_to_main_menu_keyboard,
)
from bot.keyboards.admin.admin_lessons import choose_grade_parallel_keyboard
from bot.utils.enums import AdminCallback
from bot.utils.states import LoadingLessons

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.settings import Settings
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == AdminCallback.UPLOAD_LESSONS)
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
)
async def process_lessons_handler(
    message: "Message",
    state: "FSMContext",
    settings: "Settings",
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
    await process_lessons_album_handler(message, state, settings, album)


@router.message(
    StateFilter(LoadingLessons.image),
    F.media_group_id,
    F.content_type.in_({"photo"}),
)
async def process_lessons_album_handler(
    message: "Message",
    state: "FSMContext",
    settings: "Settings",
    album: "Album",
) -> None:
    """Обработчки фотографий расписаний при нескольких штуках."""
    text, keyboard = await process_lessons_album_func(
        album,
        message.bot,
        state,
        settings.other.tesseract_path,
    )
    await message.reply(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    StateFilter(LoadingLessons.all_good),
    F.data == AdminCallback.CONFIRM,
)
async def all_good_lessons_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработка кнопки "Подтвердить" при всех верных расписаниях."""
    text, keyboard = await all_good_lessons_func(
        callback.message.chat.id,
        callback.bot,
        state,
        repo.lessons,
    )

    await callback.message.answer(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    StateFilter(LoadingLessons.all_good),
    F.data == AdminCallback.NOT_CONFIRM,
)
@router.callback_query(
    StateFilter(LoadingLessons.something_bad),
    F.data == AdminCallback.CONFIRM,
)
async def start_choose_grades_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработка кнопок для старта ручного ввода информации о расписании."""
    text, current_lesson = await start_choose_grades_func(state)

    photo = await callback.bot.send_media_group(
        chat_id=callback.message.chat.id,
        media=[InputMediaPhoto(media=current_lesson.full_photo_id)],
    )
    await photo[0].reply(
        text=text,
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
)
async def choose_grades_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок "10 классы" и "11 классы" для нераспознанных расписаний."""
    text, keyboard, current_lesson = await choose_grades_func(callback.data, state)

    photo = await callback.bot.send_media_group(
        chat_id=callback.message.chat.id,
        media=[InputMediaPhoto(media=current_lesson.full_photo_id)],
    )
    await photo[0].reply(
        text=text,
        reply_markup=keyboard,
    )


@router.message(StateFilter(LoadingLessons.choose_date))
async def choose_dates_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработка ввода даты для нераспознанных расписаний."""
    text, keyboard, media = await choose_dates_func(message.text, state)

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
    text = await confirm_edit_lessons_func(state, repo.lessons)

    await callback.message.answer(
        text=text,
        reply_markup=go_to_main_menu_keyboard,
    )
