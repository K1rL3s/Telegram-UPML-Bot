from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu
from bot.keyboards import enrollee_keyboard
from shared.utils.enums import BotMenu, SlashCommand, TextCommand

router = Router(name=__name__)


ENROLLEE_TEXT = "Привет! Я - Информация для поступающих"


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.ENROLLEE))
async def enrollee_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text=ENROLLEE_TEXT, reply_markup=enrollee_keyboard)


@router.message(F.text == TextCommand.ENROLLEE)
@router.message(Command(SlashCommand.ENROLLEE))
async def enrollee_message(message: Message) -> None:
    await message.answer(text=ENROLLEE_TEXT, reply_markup=enrollee_keyboard)
