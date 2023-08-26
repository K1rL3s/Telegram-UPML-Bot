from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from bot.keyboards.universal import cancel_state_button
from bot.utils.consts import AdminCallback


choose_meal_keyboard = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(text=dish, callback_data=callback_data)
            for dish, callback_data in zip(
                ("🕗Завтрак", "🕙Второй завтрак", "🕐Обед", "🕖Полдник", "🕖Ужин"),
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

confirm_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅Подтвердить",
                callback_data=AdminCallback.CONFIRM,
            ),
            cancel_state_button,
        ],
    ],
)
