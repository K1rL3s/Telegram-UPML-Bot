from typing import TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import LaundryData
from bot.keyboards.universal import (
    main_menu_button,
    settings_button,
)
from bot.utils.enums import Actions, UserCallback
from bot.utils.phrases import NO

if TYPE_CHECKING:
    from aiogram.utils.keyboard import InlineKeyboardMarkup

    from bot.database.models.laundries import Laundry


START_WASHING = "🏖Запустить стирку"
START_DRYING = "💨Запустить сушку"
CANCEL_TIMER = f"{NO}Отменить таймер"


async def laundry_keyboard(
    laundry: "Laundry",
    add_cancel_button: bool = True,
) -> "InlineKeyboardMarkup":
    """Клавиатура меню прачечной."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=START_WASHING,
        callback_data=LaundryData(
            action=Actions.START,
            attr=UserCallback.WASHING,
        ),
    )
    keyboard.button(
        text=START_DRYING,
        callback_data=LaundryData(
            action=Actions.START,
            attr=UserCallback.DRYING,
        ),
    )

    if add_cancel_button and laundry.is_active:
        keyboard.button(
            text=CANCEL_TIMER,
            callback_data=LaundryData(action=Actions.CANCEL),
        )

    keyboard.add(main_menu_button, settings_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
