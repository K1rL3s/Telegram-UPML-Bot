from aiogram import Dispatcher, types

from src.utils.consts import CallbackData


async def educators_view(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(
        text='😅',
        reply_markup=callback.message.reply_markup
    )


def register_educators_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        educators_view,
        text=CallbackData.OPEN_EDUCATORS
    )
