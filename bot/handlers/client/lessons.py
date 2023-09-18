from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.funcs.client.lessons import send_lessons_images
from bot.keyboards import lessons_keyboard
from bot.utils.consts import TODAY
from bot.utils.enums import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data.startswith(UserCallback.OPEN_LESSONS_ON_))
async def date_lessons_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Уроки"."""
    date_ = callback.data.replace(UserCallback.OPEN_LESSONS_ON_, "")
    lessons_date = date_by_format(date_)

    text = await send_lessons_images(
        callback.from_user.id,
        callback.message.chat.id,
        lessons_date,
        callback.bot,
        repo,
    )

    if text:
        await callback.message.edit_text(
            text=text,
            reply_markup=lessons_keyboard(lessons_date),
        )


@router.message(F.text == TextCommands.LESSONS)
@router.message(Command(SlashCommands.LESSONS))
async def date_lessons_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "Уроки"."""
    lessons_date = date_by_format(TODAY)

    text = await send_lessons_images(
        message.from_user.id,
        message.chat.id,
        lessons_date,
        message.bot,
        repo,
    )

    if text:
        await message.answer(text=text, reply_markup=lessons_keyboard(lessons_date))
