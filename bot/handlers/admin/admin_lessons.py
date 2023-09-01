from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.custom_types import Album

from bot.filters import IsAdmin
from bot.funcs.admin import process_album_lessons_func
from bot.keyboards import cancel_state_keyboard, go_to_main_menu_keyboard

from bot.utils.consts import AdminCallback
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
    text = await process_album_lessons_func(
        message.chat.id,
        album,
        settings.other.TESSERACT_PATH,
        message.bot,
        repo,
    )

    if state:
        await state.clear()

    await message.reply(text=text, reply_markup=go_to_main_menu_keyboard)
