from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.callbacks import LaundryData
from bot.keyboards.universal import main_menu_button, settings_button
from shared.database.models.laundries import Laundry
from shared.utils.enums import Action, UserCallback
from shared.utils.phrases import NO

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
            action=Action.START,
            attr=UserCallback.WASHING,
        ),
    )
    keyboard.button(
        text=START_DRYING,
        callback_data=LaundryData(
            action=Action.START,
            attr=UserCallback.DRYING,
        ),
    )

    if add_cancel_button and laundry.is_active:
        keyboard.button(
            text=CANCEL_TIMER,
            callback_data=LaundryData(action=Action.CANCEL),
        )

    keyboard.add(main_menu_button, settings_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
