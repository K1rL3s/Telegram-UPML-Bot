from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

from bot.callbacks import EditLessons
from bot.keyboards.universal import cancel_state_button
from shared.utils.enums import Grade

GRADE_10 = "10 классы"
GRADE_11 = "11 классы"


choose_parallel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=grade,
                callback_data=callback_data.pack(),
            )
            for grade, callback_data in zip(
                (GRADE_10, GRADE_11),
                (
                    EditLessons(grade=Grade.GRADE_10),
                    EditLessons(grade=Grade.GRADE_11),
                ),
            )
        ],
        [cancel_state_button],
    ],
)
