from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.handlers.client.cafe_menu.funcs import get_format_menu_by_date
from bot.keyboards import cafe_menu_keyboard
from shared.database.repository.repository import Repository
from shared.utils.consts import TODAY
from shared.utils.datehelp import date_by_format
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.CAFE_MENU))
async def cafe_menu_callback_handler(
    callback: "CallbackQuery",
    callback_data: "OpenMenu",
    repo: "Repository",
) -> None:
    """Обработчик команды кнопки "Меню", открывает расписание еды."""
    date = callback_data.date
    menu_date = date_by_format(date)

    text = await get_format_menu_by_date(repo.menu, menu_date)

    await callback.message.edit_text(
        text=text,
        reply_markup=cafe_menu_keyboard(menu_date),
    )


@router.message(F.text == TextCommand.CAFE)
@router.message(Command(SlashCommand.CAFE))
async def cafe_menu_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/cafe", открывает расписание еды."""
    menu_date = date_by_format(TODAY)

    text = await get_format_menu_by_date(repo.menu, menu_date)

    await message.answer(text=text, reply_markup=cafe_menu_keyboard(menu_date))
