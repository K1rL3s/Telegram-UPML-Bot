from datetime import date

from aiogram import Dispatcher, types

from src.handlers.cafe_menu import get_formatted_menu_by_date
from src.keyboards import cafe_menu_keyboard
from src.utils.consts import CallbackData
from src.utils.dateformat import date_by_format


async def open_today_cafe_menu(callback: types.CallbackQuery) -> None:
    text = get_formatted_menu_by_date(date.today())

    await callback.message.reply(
        text=text,
        reply_markup=cafe_menu_keyboard()
    )


async def open_date_cafe_menu(callback: types.CallbackQuery) -> None:
    menu_date = date_by_format(
        callback.data.replace(
            CallbackData.OPEN_CAFE_MENU_ON_, ''
        )
    )
    text = get_formatted_menu_by_date(menu_date)

    await callback.message.reply(
        text=text,
        reply_markup=cafe_menu_keyboard(menu_date)
    )


def register_cafe_menu_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        open_today_cafe_menu,
        lambda callback: callback.data == CallbackData.OPEN_TODAY_CAFE_MENU
    )
    dp.register_callback_query_handler(
        open_date_cafe_menu,
        lambda callback: callback.data.startswith(
            CallbackData.OPEN_CAFE_MENU_ON_
        )
    )
