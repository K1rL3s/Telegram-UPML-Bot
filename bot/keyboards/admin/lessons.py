from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton

from bot.callbacks import EditLessons
from bot.keyboards.universal import cancel_state_button
from bot.utils.enums import Grades

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
                    EditLessons(grade=Grades.GRADE_10),
                    EditLessons(grade=Grades.GRADE_11),
                ),
            )
        ],
        [cancel_state_button],
    ],
)
