from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from src.keyboards.universal import (
    cancel_state_button,
    go_to_admin_panel_button,
)
from src.utils.consts import CallbackData, GRADES


notify_panel_keyboard = InlineKeyboardBuilder().add(
    *[
        InlineKeyboardButton(
            text=for_who, callback_data=callback_data
        )
        for for_who, callback_data in zip(
            ('Всем', 'Поток', 'Класс'),
            (CallbackData.FOR_ALL, CallbackData.FOR_GRADE,
             CallbackData.FOR_CLASS)
        )
    ]
).row(
    go_to_admin_panel_button
).as_markup()

notify_for_grade_keyboard = InlineKeyboardBuilder().add(
    InlineKeyboardButton(
        text='10 классы',
        callback_data=CallbackData.DO_A_NOTIFY_FOR_ + 'grade_10'
    ),
    InlineKeyboardButton(
        text='11 классы',
        callback_data=CallbackData.DO_A_NOTIFY_FOR_ + 'grade_11'
    ),
).add(
    go_to_admin_panel_button  # сделать переход в панель уведомлений?
).as_markup()

notify_for_class_keyboard = InlineKeyboardBuilder()
for grade_letter in GRADES:
    notify_for_class_keyboard.add(
        InlineKeyboardButton(
            text=grade_letter,
            callback_data=CallbackData.DO_A_NOTIFY_FOR_ + grade_letter
        )
    )
notify_for_class_keyboard.add(
    go_to_admin_panel_button
).as_markup()

notify_confirm_keyboard = InlineKeyboardBuilder().add(
    InlineKeyboardButton(
        text='✅Подтвердить',
        callback_data=CallbackData.NOTIFY_CONFIRM
    ),
    cancel_state_button
).as_markup()
