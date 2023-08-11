from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.keyboards.universal import (
    cancel_state_button,
    go_to_admin_panel_button,
)
from bot.utils.consts import CallbackData, GRADES


notify_panel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=for_who, callback_data=callback_data)
        for for_who, callback_data in zip(
            ('Всем', 'Поток', 'Класс'),
            (CallbackData.FOR_ALL, CallbackData.FOR_GRADE,
             CallbackData.FOR_CLASS)
        )
    ],
        [go_to_admin_panel_button]
    ]
)

notify_for_grade_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='10 классы',
                callback_data=CallbackData.DO_A_NOTIFY_FOR_ + 'grade_10'
            ),
            InlineKeyboardButton(
                text='11 классы',
                callback_data=CallbackData.DO_A_NOTIFY_FOR_ + 'grade_11'
            )
        ],
        [go_to_admin_panel_button]  # сделать переход в панель уведомлений?
    ]
)

notify_for_class_keyboard = InlineKeyboardBuilder().add(
    *[
        InlineKeyboardButton(
            text=grade_letter,
            callback_data=CallbackData.DO_A_NOTIFY_FOR_ + grade_letter
        )
        for grade_letter in GRADES
    ],
    go_to_admin_panel_button
).adjust(3, 3, 1).as_markup()

notify_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='✅Подтвердить',
                callback_data=CallbackData.NOTIFY_CONFIRM
            )
        ],
        [cancel_state_button]
    ]
)
