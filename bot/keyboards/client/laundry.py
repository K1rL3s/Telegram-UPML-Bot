from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
)

from bot.keyboards.universal import (
    go_to_main_menu_button,
    go_to_settings_button,
)
from bot.utils.enums import UserCallback
from bot.utils.phrases import NO


if TYPE_CHECKING:
    from aiogram.utils.keyboard import InlineKeyboardMarkup

    from bot.database.models.laundries import Laundry


START_WASHING = "🏖Запустить стирку"
START_DRYING = "💨Запустить сушку"
STOP_TIMER = f"{NO}Отменить таймер"


async def laundry_keyboard(
    laundry: "Laundry",
    add_cancel_button: bool = True,
) -> "InlineKeyboardMarkup":
    """Клавиатура меню прачечной."""
    keyboard = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text=START_WASHING,
            callback_data=UserCallback.START_WASHING_TIMER,
        ),
        InlineKeyboardButton(
            text=START_DRYING,
            callback_data=UserCallback.START_DRYING_TIMER,
        ),
    )

    if add_cancel_button and laundry.is_active:
        keyboard.add(
            InlineKeyboardButton(
                text=STOP_TIMER,
                callback_data=UserCallback.CANCEL_LAUNDRY_TIMER,
            ),
        )

    keyboard.add(go_to_main_menu_button, go_to_settings_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
