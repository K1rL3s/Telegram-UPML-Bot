from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.database.repository.repository import Repository
from bot.funcs.laundry import (
    laundry_cancel_timer_func,
    laundry_welcome_func,
    laundry_start_timer_func,
)
from bot.keyboards import go_to_main_menu_keyboard, laundry_keyboard
from bot.utils.consts import (
    UserCallback,
    SlashCommands,
    TextCommands,
    LAUNDRY_REPEAT,
)
from bot.utils.datehelp import format_datetime


router = Router(name=__name__)


@router.message(F.text == TextCommands.LAUNDRY)
@router.message(Command(SlashCommands.LAUNDRY))
@router.callback_query(F.data == UserCallback.OPEN_LAUNDRY)
async def laundry_handler(
    callback: CallbackQuery | Message,
    repo: Repository,
) -> None:
    """
    Обработчик кнопки "Прачечная".
    """
    text = (
        "Привет! Я - таймер для прачки.\n"
        "После конца таймер запустится ещё три раза "
        f"на *{LAUNDRY_REPEAT}* минут.\n\n"
    )

    laundry = await repo.laundry.get_laundry(callback.from_user.id)

    if (minutes := await laundry_welcome_func(laundry)) is None:
        text += f"Время до конца таймера: *{minutes}* минут\n"

    keyboard = await laundry_keyboard(laundry)
    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(text=text.strip(), reply_markup=keyboard)
    else:
        await callback.answer(text=text.strip(), reply_markup=keyboard)


@router.callback_query(F.data.startswith(UserCallback.START_LAUNDRY_PREFIX))
async def laundry_start_timer_handler(
    callback: CallbackQuery,
    repo: Repository,
) -> None:
    """
    Обработчик кнопок "Запустить стирку", "Запустить сушку".
    """
    minutes, end_time = await laundry_start_timer_func(
        repo, callback.from_user.id, callback.data
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
    callback: CallbackQuery,
    repo: Repository,
) -> None:
    """
    Обработчик кнопки "Отменить таймер".
    """
    await laundry_cancel_timer_func(repo, callback.from_user.id)
    text = "Таймер отменён."
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(text=text, reply_markup=keyboard)
