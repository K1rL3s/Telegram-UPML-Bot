from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)
from bot.keyboards.universal import cancel_state_button
from bot.utils.consts import BEAUTIFY_MEALS
from bot.utils.enums import AdminCallback


choose_meal_keyboard = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(text=dish, callback_data=callback_data)
            for dish, callback_data in zip(
                BEAUTIFY_MEALS,
                (
                    AdminCallback.EDIT_BREAKFAST,
                    AdminCallback.EDIT_LUNCH,
                    AdminCallback.EDIT_DINNER,
                    AdminCallback.EDIT_SNACK,
                    AdminCallback.EDIT_SUPPER,
                ),
            )
        ),
        cancel_state_button,
    )
    .adjust(3, 2, 1)
    .as_markup()
)
