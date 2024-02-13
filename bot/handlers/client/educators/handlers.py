from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.handlers.client.educators.funcs import get_format_educators_by_date
from bot.keyboards import educators_keyboard
from shared.database.repository.repository import Repository
from shared.utils.consts import TODAY
from shared.utils.datehelp import date_by_format
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.EDUCATORS))
async def educators_callback_handler(
    callback: "CallbackQuery",
    callback_data: "OpenMenu",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Воспитатели"."""
    date_ = callback_data.date
    schedule_date = date_by_format(date_)

    text = await get_format_educators_by_date(repo.educators, schedule_date)

    await callback.message.edit_text(
        text=text,
        reply_markup=educators_keyboard(schedule_date),
    )


@router.message(F.text == TextCommand.EDUCATORS)
@router.message(Command(SlashCommand.EDUCATORS))
async def educators_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/educators"."""
    schedule_date = date_by_format(TODAY)

    text = await get_format_educators_by_date(repo.educators, schedule_date)

    await message.answer(
        text=text,
        reply_markup=educators_keyboard(schedule_date),
    )
