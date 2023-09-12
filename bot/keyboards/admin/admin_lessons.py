from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

from bot.keyboards.universal import (
    cancel_state_button,
)
from bot.utils.enums import AdminCallback


GRADE_10 = "10 классы"
GRADE_11 = "11 классы"


choose_grade_parallel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{grade}",
                callback_data=callback_data,
            )
            for grade, callback_data in zip(
                (GRADE_10, GRADE_11),
                (
                    AdminCallback.UPLOAD_LESSONS_FOR_10,
                    AdminCallback.UPLOAD_LESSONS_FOR_11,
                ),
            )
        ],
        [cancel_state_button],
    ],
)
