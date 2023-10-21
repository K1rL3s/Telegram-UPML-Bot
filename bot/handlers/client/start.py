from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from bot.callbacks import OpenMenu
from bot.keyboards import main_menu_keyboard, start_reply_keyboard
from bot.middlewares.inner.save_user import SaveUpdateUserMiddleware
from bot.utils.phrases import MAIN_MENU_TEXT, USER_START_TEXT
from bot.utils.enums import Menus, SlashCommands, TextCommands

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message
    from aiogram.fsm.context import FSMContext

    from bot.database.repository.repository import Repository


router = Router(name=__name__)
router.message.middleware(SaveUpdateUserMiddleware())


@router.message(F.text == TextCommands.START, StateFilter("*"))
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(
    message: "Message",
    repo: "Repository",
    state: "FSMContext",
) -> None:
    """Обработчик команды "/start"."""
    await state.clear()
    await message.reply(
        text=USER_START_TEXT,
        reply_markup=await start_reply_keyboard(repo.user, message.from_user.id),
    )


@router.callback_query(OpenMenu.filter(F.menu == Menus.MAIN_MENU))
async def main_menu_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Главное меню"."""
    keyboard = await main_menu_keyboard(repo.user, callback.from_user.id)
    await callback.message.edit_text(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommands.MENU)
@router.message(Command(SlashCommands.MENU))
async def main_menu_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/menu"."""
    keyboard = await main_menu_keyboard(repo.user, message.from_user.id)
    await message.reply(text=MAIN_MENU_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommands.HELP)
@router.message(Command(SlashCommands.HELP))
async def help_handler(message: "Message") -> None:
    """Обработчик команды "/help"."""
    await message.reply("Помощь!")
