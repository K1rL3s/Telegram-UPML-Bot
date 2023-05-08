from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.consts import CallbackData


cancel_state_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        '❌Отмена',
        callback_data=CallbackData.CANCEL_STATE
    )
)
