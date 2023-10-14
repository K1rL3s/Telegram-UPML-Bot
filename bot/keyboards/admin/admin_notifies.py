from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from bot.callbacks import DoNotifyData
from bot.keyboards.universal import go_to_admin_panel_button
from bot.utils.consts import GRADES
from bot.utils.enums import NotifyTypes


notify_panel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=for_who, callback_data=callback_data.pack())
            for for_who, callback_data in zip(
                ("Всем", "Поток", "Класс"),
                (
                    DoNotifyData(for_who=NotifyTypes.ALL),
                    DoNotifyData(notify_type=NotifyTypes.GRADE),
                    DoNotifyData(notify_type=NotifyTypes.CLASS),
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
                callback_data=DoNotifyData(for_who=NotifyTypes.GRADE_10).pack(),
            ),
            InlineKeyboardButton(
                text="11 классы",
                callback_data=DoNotifyData(for_who=NotifyTypes.GRADE_11).pack(),
            ),
        ],
        [go_to_admin_panel_button],  # сделать переход в панель уведомлений?
    ],
)

notify_for_class_keyboard: "InlineKeyboardMarkup" = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=grade_letter,
                callback_data=DoNotifyData(for_who=grade_letter).pack(),
            )
            for grade_letter in GRADES
        ),
        go_to_admin_panel_button,
    )
    .adjust(3, 3, 1)
    .as_markup()
)
