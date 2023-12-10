from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.callbacks import OpenMenu
from bot.funcs.client.lessons import send_lessons_images
from bot.keyboards import lessons_keyboard
from bot.utils.consts import TODAY
from bot.utils.datehelp import date_by_format
from bot.utils.enums import Menus, SlashCommands, TextCommands

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == Menus.LESSONS))
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


@router.message(F.text == TextCommands.LESSONS)
@router.message(Command(SlashCommands.LESSONS))
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
