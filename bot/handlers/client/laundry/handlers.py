from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import LaundryData, OpenMenu
from bot.keyboards import go_to_main_menu_keyboard
from shared.database.repository.repository import Repository
from shared.utils.datehelp import format_datetime
from shared.utils.enums import Action, BotMenu, SlashCommand, TextCommand

from .funcs import laundry_func, laundry_start_timer_func

router = Router(name=__name__)


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.LAUNDRY))
async def laundry_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Прачечная"."""
    text, keyboard = await laundry_func(callback.from_user.id, repo.laundry)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.message(F.text == TextCommand.LAUNDRY)
@router.message(Command(SlashCommand.LAUNDRY))
async def laundry_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "Прачечная"."""
    text, keyboard = await laundry_func(message.from_user.id, repo.laundry)
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(LaundryData.filter(F.action == Action.START))
async def laundry_start_timer_handler(
    callback: "CallbackQuery",
    callback_data: "LaundryData",
    repo: "Repository",
) -> None:
    """Обработчик кнопок "Запустить стирку", "Запустить сушку"."""
    minutes, end_time = await laundry_start_timer_func(
        repo.settings,
        repo.laundry,
        callback.from_user.id,
        callback_data.attr,
    )

    text = (
        f"⏰Таймер запущен!\n"
        f"Уведомление придёт через <b>~{minutes} минут</b> "
        f"({format_datetime(end_time)})"
    )
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(LaundryData.filter(F.action == Action.CANCEL))
async def laundry_cancel_timer_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Отменить таймер"."""
    await repo.laundry.cancel_timer(callback.from_user.id)

    text = "Таймер отменён."
    _, keyboard = await laundry_func(callback.from_user.id, repo.laundry)

    await callback.message.edit_text(text=text, reply_markup=keyboard)
