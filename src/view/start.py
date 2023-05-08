from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.database.db_funcs import save_user_or_update_status
from src.keyboards import start_menu_keyboard, main_menu_keyboard
from src.utils.consts import CallbackData


async def start_view(message: types.Message) -> None:
    save_user_or_update_status(message.from_user.id)

    text = 'Привет! Я - стартовое меню.'

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


async def main_menu_view(message: types.Message | types.CallbackQuery) -> None:
    text = 'Привет! Я - главное меню.'

    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(
            text=text,
            reply_markup=main_menu_keyboard
        )
    else:
        await message.reply(
            text=text,
            reply_markup=main_menu_keyboard
        )


async def cancel_state(
        message: types.Message | types.CallbackQuery,
        state: FSMContext
) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await main_menu_view(message)


def register_start_view(dp: Dispatcher):
    dp.register_message_handler(
        cancel_state,
        commands=['cancel', 'stop'],
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_state,
        text=CallbackData.CANCEL_STATE,
        state='*'
    )
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
