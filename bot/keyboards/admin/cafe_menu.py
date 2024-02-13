from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import EditMeal
from bot.keyboards.universal import cancel_state_button
from shared.utils.consts import BEAUTIFY_MEALS
from shared.utils.enums import Meal

choose_meal_keyboard: "InlineKeyboardMarkup" = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(text=dish, callback_data=callback_data.pack())
            for dish, callback_data in zip(
                BEAUTIFY_MEALS,
                (
                    EditMeal(meal=Meal.BREAKFAST),
                    EditMeal(meal=Meal.LUNCH),
                    EditMeal(meal=Meal.DINNER),
                    EditMeal(meal=Meal.SNACK),
                    EditMeal(meal=Meal.SUPPER),
                ),
            )
        ),
        cancel_state_button,
    )
    .adjust(3, 2, 1)
    .as_markup()
)
