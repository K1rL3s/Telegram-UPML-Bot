from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.funcs.cafe_menu import get_format_menu_by_date
from bot.keyboards import cafe_menu_keyboard
from bot.utils.enums import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data.startswith(UserCallback.OPEN_CAFE_MENU_ON_))
async def date_cafe_menu_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик команды кнопки "Меню", открывает расписание еды."""
    date_ = callback.data.replace(UserCallback.OPEN_CAFE_MENU_ON_, "")
    menu_date = date_by_format(date_)

    text = await get_format_menu_by_date(repo.menu, menu_date)

    await callback.message.edit_text(
        text=text,
        reply_markup=cafe_menu_keyboard(menu_date),
    )


@router.message(F.text == TextCommands.CAFE)
@router.message(Command(SlashCommands.CAFE))
async def date_cafe_menu_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/cafe", открывает расписание еды."""
    date_ = "today"
    menu_date = date_by_format(date_)

    text = await get_format_menu_by_date(repo.menu, menu_date)

    await message.answer(text=text, reply_markup=cafe_menu_keyboard(menu_date))
