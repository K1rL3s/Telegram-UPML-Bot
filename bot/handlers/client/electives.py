from typing import TYPE_CHECKING, Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards import main_menu_inline_keyboard
from bot.utils.consts import SlashCommands, TextCommands, UserCallback

if TYPE_CHECKING:
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.message(F.text == TextCommands.ELECTIVES)
@router.message(Command(SlashCommands.ELECTIVES))
@router.callback_query(F.data == UserCallback.OPEN_ELECTIVES)
async def electives_handler(
    callback: "Union[CallbackQuery, Message]",
    repo: "Repository",
) -> None:
    """Обработчик команды "/electives" и кнопки "Элективы"."""
    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text="🥲",
            reply_markup=callback.message.reply_markup,
        )
    else:
        await callback.answer(
            text="🥲",
            reply_markup=await main_menu_inline_keyboard(repo, callback.from_user.id),
        )
