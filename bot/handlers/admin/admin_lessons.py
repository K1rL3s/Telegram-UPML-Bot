from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.custom_types import Album
from bot.database.db_funcs import Repository
from bot.filters import IsAdmin
from bot.funcs.admin import load_album_lessons_func
from bot.keyboards import cancel_state_keyboard, go_to_main_menu_keyboard
from bot.utils.consts import CallbackData
from bot.utils.states import LoadingLessons


router = Router(name=__name__)


@router.callback_query(F.data == CallbackData.UPLOAD_LESSONS, IsAdmin())
async def start_load_lessons_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик кнопки "Загрузить уроки".
    """
    await state.set_state(LoadingLessons.image)
    text = 'Отправьте изображение(-я) расписания уроков'

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(
    StateFilter(LoadingLessons.image),
    F.content_type.in_({'photo'}),
    IsAdmin(),
)
async def load_lessons_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
) -> None:
    album = Album.model_validate(
        {
            "photo": [message.photo[-1]],
            "messages": [message],
            "caption": message.html_text,
        },
        context={"bot": message.bot}
    )
    await load_lessons_album_handler(message, state, repo, album)


@router.message(
    StateFilter(LoadingLessons.image),
    F.media_group_id,
    IsAdmin(),
)
async def load_lessons_album_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
        album: Album,
) -> None:
    """
    Обработчик сообщений с изображениями
    после нажатия кнопки "Загрузить уроки".
    """

    text = await load_album_lessons_func(
        message.chat.id, album, message.bot, repo
    )

    if state:
        await state.clear()

    await message.reply(
        text=text,
        reply_markup=go_to_main_menu_keyboard
    )
