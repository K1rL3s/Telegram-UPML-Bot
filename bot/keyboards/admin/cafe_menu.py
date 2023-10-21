from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import EditMeal
from bot.keyboards.universal import cancel_state_button
from bot.utils.consts import BEAUTIFY_MEALS
from bot.utils.enums import Meals


choose_meal_keyboard: "InlineKeyboardMarkup" = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(text=dish, callback_data=callback_data.pack())
            for dish, callback_data in zip(
                BEAUTIFY_MEALS,
                (
                    EditMeal(meal=Meals.BREAKFAST),
                    EditMeal(meal=Meals.LUNCH),
                    EditMeal(meal=Meals.DINNER),
                    EditMeal(meal=Meals.SNACK),
                    EditMeal(meal=Meals.SUPPER),
                ),
            )
        ),
        cancel_state_button,
    )
    .adjust(3, 2, 1)
    .as_markup()
)
