from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import lessons_keyboard
from shared.database.repository.repository import Repository
from shared.utils.consts import TODAY
from shared.utils.datehelp import date_by_format
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

from .funcs import send_lessons_images

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.LESSONS))
async def lessons_callback_handler(
    callback: "CallbackQuery",
    callback_data: "OpenMenu",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Уроки"."""
    date_ = callback_data.date
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


@router.message(F.text == TextCommand.LESSONS)
@router.message(Command(SlashCommand.LESSONS))
async def lessons_message_handler(
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
