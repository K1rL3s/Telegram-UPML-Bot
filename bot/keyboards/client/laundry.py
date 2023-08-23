from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.database.models.laundries import Laundry
from bot.keyboards.universal import (
    go_to_main_menu_button,
    go_to_settings_button,
)
from bot.utils.consts import UserCallback


async def laundry_keyboard(
    laundry: Laundry, add_cancel_if_timer: bool = True
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="🏖Запустить стирку", callback_data=UserCallback.START_WASHING_TIMER
        ),
        InlineKeyboardButton(
            text="💨Запустить сушку", callback_data=UserCallback.START_DRYING_TIMER
        ),
    )

    if add_cancel_if_timer and laundry.is_active:
        keyboard.add(
            InlineKeyboardButton(
                text="❌Отменить таймер", callback_data=UserCallback.CANCEL_LAUNDRY_TIMER
            )
        )

    keyboard.add(go_to_main_menu_button, go_to_settings_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
