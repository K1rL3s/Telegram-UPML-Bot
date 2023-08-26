from typing import TYPE_CHECKING, Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from bot.filters import SaveUser
from bot.funcs.lessons import get_lessons_for_user
from bot.keyboards import lessons_keyboard
from bot.utils.consts import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.message(F.text == TextCommands.LESSONS, SaveUser())
@router.message(Command(SlashCommands.LESSONS), SaveUser())
@router.callback_query(
    F.data.startswith(UserCallback.OPEN_LESSONS_ON_),
    SaveUser(),
)
async def open_date_lessons_handler(
    callback: "Union[CallbackQuery, Message]",
    repo: "Repository",
) -> None:
    """
    Обработчик кнопки "Уроки".

    Отправляет расписание уроков паралелли и класса, если выбран класс.
    Отправляет расписание двух паралеллей, если не выбран класс.
    """
    if isinstance(callback, CallbackQuery):
        date_ = callback.data.replace(UserCallback.OPEN_LESSONS_ON_, "")
    else:
        date_ = "today"
    lessons_date = date_by_format(date_)

    text, images = await get_lessons_for_user(repo, callback.from_user.id, lessons_date)

    if any(images):
        messages = await callback.bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=[InputMediaPhoto(media=media_id) for media_id in images if media_id],
        )
        await messages[0].reply(text=text, reply_markup=lessons_keyboard(lessons_date))
        return

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date),
        )
    else:
        await callback.answer(text=text, reply_markup=lessons_keyboard(lessons_date))
