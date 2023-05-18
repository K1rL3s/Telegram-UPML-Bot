from aiogram import Dispatcher, types

from src.handlers.laundry import (
    laundry_cancel_timer_handler, laundry_welcome_handler,
    laundry_start_timer_handler,
)
from src.keyboards import go_to_main_menu_keyboard, laundry_keyboard
from src.utils.consts import CallbackData
from src.utils.datehelp import format_datetime


async def laundry_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Прачечная".
    """
    text = 'Привет! Я - таймер для прачки.\n\n'

    if (minutes := laundry_welcome_handler(callback.from_user.id)) is not None:
        text += f'Время до конца таймера: *{minutes}* минут'

    keyboard = laundry_keyboard(callback.from_user.id)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def laundry_start_timer_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопок "Запустить стирку", "Запустить сушку".
    """
    minutes, end_time = laundry_start_timer_handler(
        callback.from_user.id, callback.data
    )

    text = f'⏰Таймер запущен!\n' \
           f'Уведомление придёт через *~{minutes} минут* ' \
           f'({format_datetime(end_time)})'
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def laundry_cancel_timer_view(callback: types.CallbackQuery) -> None:
    laundry_cancel_timer_handler(callback.from_user.id)
    text = 'Таймер отменён.'
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


def register_laundry_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        laundry_view,
        text=CallbackData.OPEN_LAUNDRY
    )
    dp.register_callback_query_handler(
        laundry_start_timer_view,
        lambda callback: callback.data.startswith(
            CallbackData.START_LAUNDRY_PREFIX
        )
    )
    dp.register_callback_query_handler(
        laundry_cancel_timer_view,
        text=CallbackData.CANCEL_LAUNDRY_TIMER
    )
