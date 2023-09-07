from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.funcs.client.educators import get_format_educators_by_date
from bot.keyboards import educators_keyboard
from bot.utils.enums import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data.startswith(UserCallback.OPEN_EDUCATORS_ON_))
async def educators_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Воспитатели"."""
    date_ = callback.data.replace(UserCallback.OPEN_EDUCATORS_ON_, "")
    schedule_date = date_by_format(date_)

    text = await get_format_educators_by_date(repo.educators, schedule_date)

    await callback.message.edit_text(
        text=text,
        reply_markup=educators_keyboard(schedule_date),
    )


@router.message(F.text == TextCommands.EDUCATORS)
@router.message(Command(SlashCommands.EDUCATORS))
async def educators_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/educators"."""
    date_ = "today"
    schedule_date = date_by_format(date_)

    text = await get_format_educators_by_date(repo.educators, schedule_date)

    await message.answer(
        text=text,
        reply_markup=educators_keyboard(schedule_date),
    )
