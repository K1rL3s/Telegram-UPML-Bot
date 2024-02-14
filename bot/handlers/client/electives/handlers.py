from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import main_menu_keyboard
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.ELECTIVES))
async def electives_callback_handler(
    callback: "CallbackQuery",
) -> None:
    """Обработчик кнопки "Элективы"."""
    await callback.message.edit_text(
        text="🥲",
        reply_markup=callback.message.reply_markup,
    )


@router.message(F.text == TextCommand.ELECTIVES)
@router.message(Command(SlashCommand.ELECTIVES))
async def electives_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/electives"."""
    await message.answer(
        text="🥲",
        reply_markup=await main_menu_keyboard(repo.user, message.from_user.id),
    )
