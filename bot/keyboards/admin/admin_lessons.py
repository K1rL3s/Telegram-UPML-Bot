from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

from bot.keyboards.universal import (
    cancel_state_button,
)
from bot.utils.enums import AdminCallback


choose_grade_parallel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{grade}",
                callback_data=callback_data,
            )
            for grade, callback_data in zip(
                ("10 классы", "11 классы"),
                (
                    AdminCallback.UPLOAD_LESSONS_FOR_10,
                    AdminCallback.UPLOAD_LESSONS_FOR_11,
                ),
            )
        ],
        [cancel_state_button],
    ],
)
