from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import InStateData
from bot.handlers.client.start.handlers import (
    main_menu_callback_handler,
    main_menu_message_handler,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import Action, SlashCommand, TextCommand

router = Router(name=__name__)


@router.callback_query(
    InStateData.filter(F.action == Action.CANCEL),
    StateFilter("*"),
)
async def cancel_callback_state(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопок с отменой состояний."""
    if await state.get_state() is None:
        return

    await state.clear()

    await main_menu_callback_handler(callback, repo)


@router.message(F.text == TextCommand.CANCEL, StateFilter("*"))
@router.message(
    Command(SlashCommand.CANCEL, SlashCommand.STOP),
    StateFilter("*"),
)
async def cancel_message_text(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик команд "/cancel", "/stop"."""
    if await state.get_state() is None:
        return

    await state.clear()

    await main_menu_message_handler(message, repo)
