from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.callbacks import DoNotify
from bot.keyboards.universal import admin_panel_button
from shared.utils.consts import GRADES
from shared.utils.enums import NotifyType

notify_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=for_who, callback_data=callback_data.pack())
            for for_who, callback_data in zip(
                ("Всем", "Поток", "Класс"),
                (
                    DoNotify(for_who=NotifyType.ALL),
                    DoNotify(notify_type=NotifyType.GRADE),
                    DoNotify(notify_type=NotifyType.CLASS),
                ),
            )
        ],
        [admin_panel_button],
    ],
)

notify_for_grade_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="10 классы",
                callback_data=DoNotify(for_who=NotifyType.GRADE_10).pack(),
            ),
            InlineKeyboardButton(
                text="11 классы",
                callback_data=DoNotify(for_who=NotifyType.GRADE_11).pack(),
            ),
        ],
        [admin_panel_button],  # сделать переход в панель уведомлений?
    ],
)

notify_for_class_keyboard: "InlineKeyboardMarkup" = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=grade_letter,
                callback_data=DoNotify(for_who=grade_letter).pack(),
            )
            for grade_letter in GRADES
        ),
        admin_panel_button,
    )
    .adjust(3, 3, 1)
    .as_markup()
)
