from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.funcs.laundry import (
    laundry_cancel_timer_func,
    laundry_start_timer_func,
    laundry_welcome_func,
)
from bot.keyboards import go_to_main_menu_keyboard, laundry_keyboard
from bot.utils.consts import LAUNDRY_REPEAT
from bot.utils.enums import SlashCommands, TextCommands, UserCallback
from bot.utils.datehelp import format_datetime

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

    from bot.database.repository.repository import Repository
    from bot.database.repository import LaundryRepository


router = Router(name=__name__)


async def laundry_handler(
    user_id: int,
    repo: "LaundryRepository",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Текст и клавиатура при переходе в таймеры для прачечной.

    :param user_id: ТГ Айди.
    :param repo: Репозиторий таймеров прачечной.
    :return: Сообщение пользователю и клавиатура.
    """
    text = f"""Привет! Я - таймер для прачечной.
После конца таймер запустится ещё три раза на *{LAUNDRY_REPEAT}* минут."""

    laundry = await repo.get(user_id)
    keyboard = await laundry_keyboard(laundry)

    if (minutes := await laundry_welcome_func(laundry)) is not None:
        text += f"\n\nВремя до конца таймера: *{minutes}* минут"

    return text, keyboard


@router.callback_query(F.data == UserCallback.OPEN_LAUNDRY)
async def laundry_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Прачечная"."""
    text, keyboard = await laundry_handler(callback.from_user.id, repo.laundry)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.message(F.text == TextCommands.LAUNDRY)
@router.message(Command(SlashCommands.LAUNDRY))
async def laundry_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Прачечная"."""
    text, keyboard = await laundry_handler(message.from_user.id, repo.laundry)
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(F.data.startswith(UserCallback.START_LAUNDRY_PREFIX))
async def laundry_start_timer_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопок "Запустить стирку", "Запустить сушку"."""
    minutes, end_time = await laundry_start_timer_func(
        repo.settings,
        repo.laundry,
        callback.from_user.id,
        callback.data,
    )

    text = (
        f"⏰Таймер запущен!\n"
        f"Уведомление придёт через *~{minutes} минут* "
        f"({format_datetime(end_time)})"
    )
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data == UserCallback.CANCEL_LAUNDRY_TIMER)
async def laundry_cancel_timer_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Отменить таймер"."""
    await laundry_cancel_timer_func(repo.laundry, callback.from_user.id)
    text = "Таймер отменён."
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(text=text, reply_markup=keyboard)
