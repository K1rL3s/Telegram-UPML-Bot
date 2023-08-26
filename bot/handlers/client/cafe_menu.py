from typing import TYPE_CHECKING, Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.funcs.cafe_menu import get_format_menu_by_date
from bot.keyboards import cafe_menu_keyboard
from bot.utils.consts import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import date_by_format

if TYPE_CHECKING:
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.message(F.text == TextCommands.CAFE)
@router.message(Command(SlashCommands.CAFE))
@router.callback_query(F.data.startswith(UserCallback.OPEN_CAFE_MENU_ON_))
async def open_date_cafe_menu(
    callback: "Union[CallbackQuery, Message]",
    repo: "Repository",
) -> None:
    """Обработчик команды "/cafe" и кнопки "Меню", открывает расписание еды."""
    if isinstance(callback, CallbackQuery):
        date_ = callback.data.replace(UserCallback.OPEN_CAFE_MENU_ON_, "")
    else:
        date_ = "today"
    menu_date = date_by_format(date_)

    text = await get_format_menu_by_date(repo, menu_date)

    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text=text,
            reply_markup=cafe_menu_keyboard(menu_date),
        )
    else:
        await callback.answer(text=text, reply_markup=cafe_menu_keyboard(menu_date))
