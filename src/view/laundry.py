from aiogram import F, Router, types
from aiogram.filters import Command

from src.handlers.laundry import (
    laundry_cancel_timer_handler, laundry_welcome_handler,
    laundry_start_timer_handler,
)
from src.keyboards import go_to_main_menu_keyboard, laundry_keyboard
from src.utils.consts import CallbackData, Commands, LAUNDRY_REPEAT
from src.utils.datehelp import format_datetime


router = Router(name='laundry')


@router.message(Command(Commands.LAUNDRY))
@router.callback_query(F.data == CallbackData.OPEN_LAUNDRY)
async def laundry_view(
        callback: types.CallbackQuery | types.Message
) -> None:
    """
    Обработчик кнопки "Прачечная".
    """
    text = 'Привет! Я - таймер для прачки.\n' \
           'После конца таймер запустится ещё три раза ' \
           f'на *{LAUNDRY_REPEAT}* минут.\n\n'

    minutes = await laundry_welcome_handler(callback.from_user.id)
    if minutes is not None:
        text += f'Время до конца таймера: *{minutes}* минут\n'

    keyboard = await laundry_keyboard(callback.from_user.id)

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_text(
            text=text.strip(),
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text=text.strip(),
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith(CallbackData.START_LAUNDRY_PREFIX))
async def laundry_start_timer_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопок "Запустить стирку", "Запустить сушку".
    """
    minutes, end_time = await laundry_start_timer_handler(
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


@router.callback_query(F.data == CallbackData.CANCEL_LAUNDRY_TIMER)
async def laundry_cancel_timer_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Отменить таймер".
    """
    await laundry_cancel_timer_handler(callback.from_user.id)
    text = 'Таймер отменён.'
    keyboard = go_to_main_menu_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
