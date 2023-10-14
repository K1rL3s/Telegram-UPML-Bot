from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import EditMealData
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
                    EditMealData(meal=Meals.BREAKFAST),
                    EditMealData(meal=Meals.LUNCH),
                    EditMealData(meal=Meals.DINNER),
                    EditMealData(meal=Meals.SNACK),
                    EditMealData(meal=Meals.SUPPER),
                ),
            )
        ),
        cancel_state_button,
    )
    .adjust(3, 2, 1)
    .as_markup()
)
