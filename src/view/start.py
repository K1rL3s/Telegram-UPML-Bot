from aiogram import Dispatcher, types

from src.keyboards import start_menu_keyboard
from src.utils.consts import CallbackData


async def start_view(message: types.Message) -> None:
    text = 'Привет! Я - стартовое меню.'

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


async def main_menu_view(message: types.Message | types.CallbackQuery) -> None:
    text = 'Привет! Я - главное меню.'

    if isinstance(message, types.CallbackQuery):
        message = message.message

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


def register_base_view(dp: Dispatcher):
    dp.register_message_handler(
        start_view,
        commands=['start'],
    )
    dp.register_message_handler(
        main_menu_view,
        commands=['menu'],
    )
    dp.register_callback_query_handler(
        main_menu_view,
        text=CallbackData.OPEN_MAIN_MENU
    )
