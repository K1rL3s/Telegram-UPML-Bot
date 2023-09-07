from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.keyboards.universal import go_to_admin_panel_button
from bot.utils.consts import GRADES
from bot.utils.enums import AdminCallback, NotifyTypes


notify_panel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=for_who, callback_data=callback_data)
            for for_who, callback_data in zip(
                ("Всем", "Поток", "Класс"),
                (
                    AdminCallback.NOTIFY_FOR_ALL,
                    AdminCallback.NOTIFY_FOR_GRADE,
                    AdminCallback.NOTIFY_FOR_CLASS,
                ),
            )
        ],
        [go_to_admin_panel_button],
    ],
)

notify_for_grade_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="10 классы",
                callback_data=AdminCallback.DO_A_NOTIFY_FOR_ + NotifyTypes.GRADE_10,
            ),
            InlineKeyboardButton(
                text="11 классы",
                callback_data=AdminCallback.DO_A_NOTIFY_FOR_ + NotifyTypes.GRADE_11,
            ),
        ],
        [go_to_admin_panel_button],  # сделать переход в панель уведомлений?
    ],
)

notify_for_class_keyboard = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=grade_letter,
                callback_data=AdminCallback.DO_A_NOTIFY_FOR_ + grade_letter,
            )
            for grade_letter in GRADES
        ),
        go_to_admin_panel_button,
    )
    .adjust(3, 3, 1)
    .as_markup()
)
