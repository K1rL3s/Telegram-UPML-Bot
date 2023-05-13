from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.universal import cancel_state_button
from src.utils.consts import CallbackData


choose_meal_keyboard = InlineKeyboardMarkup(row_width=3).add(
    *[InlineKeyboardButton(dish, callback_data=callback_data)
      for dish, callback_data in zip(
            ('🕗Завтрак', '🕙Второй завтрак',
             '🕐Обед', '🕖Полдник',
             '🕖Ужин'),
            (CallbackData.EDIT_BREAKFAST, CallbackData.EDIT_LUNCH,
             CallbackData.EDIT_DINNER, CallbackData.EDIT_SNACK,
             CallbackData.EDIT_SUPPER)
        )
      ]
).add(
    cancel_state_button
)
confirm_edit_menu_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        '✅Подтвердить',
        callback_data=CallbackData.EDIT_CONFIRM
    ),
    cancel_state_button
)
