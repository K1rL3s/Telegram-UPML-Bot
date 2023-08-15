from aiogram import F, Router
from aiogram.filters import Command
from aiogram.methods import SendMediaGroup
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from bot.database.db_funcs import Repository
from bot.filters import SaveUser
from bot.funcs.lessons import get_lessons_text_and_image_id
from bot.keyboards import lessons_keyboard
from bot.utils.consts import CallbackData, SlashCommands, TextCommands
from bot.utils.datehelp import date_by_format


router = Router(name=__name__)


@router.message(F.text == TextCommands.LESSONS, SaveUser())
@router.message(Command(SlashCommands.LESSONS), SaveUser())
@router.callback_query(
    F.data.startswith(CallbackData.OPEN_LESSONS_ON_),
    SaveUser(),
)
async def open_date_lessons_handler(
        callback: CallbackQuery | Message,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки "Уроки".
    Отправляет расписание уроков паралелли и класса, если выбран класс.
    Отправляет расписание двух паралеллей, если не выбран класс.
    """

    if isinstance(callback, CallbackQuery):
        _date = callback.data.replace(CallbackData.OPEN_LESSONS_ON_, '')
    else:
        _date = 'today'
    lessons_date = date_by_format(_date)

    text, images = await get_lessons_text_and_image_id(
        repo, callback.from_user.id, lessons_date
    )

    if images:
        messages = await SendMediaGroup(
            chat_id=callback.message.chat.id,
            media=[
                InputMediaPhoto(media=media_id)
                for media_id in images
                if media_id
            ]
        )
        await messages[0].reply(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )
        return

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )
    else:
        await callback.answer(
            text=text,
            reply_markup=lessons_keyboard(lessons_date)
        )