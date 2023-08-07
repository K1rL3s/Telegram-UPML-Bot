from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.database.db_funcs import get_settings
from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData, GRADES


async def settings_keyboard(user_id: int) -> InlineKeyboardMarkup:
    settings = await get_settings(user_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Класс ' + (
                        settings.class_ if settings.class_ else '❓'
                    ),
                    callback_data=CallbackData.CHANGE_GRADE_TO_
                ),
                InlineKeyboardButton(
                    text='Уроки ' + ('✅' if settings.lessons_notify else '❌'),
                    callback_data=CallbackData.SWITCH_LESSONS_NOTIFY
                ),
                InlineKeyboardButton(
                    text='Новости ' + ('✅' if settings.news_notify else '❌'),
                    callback_data=CallbackData.SWITCH_NEWS_NOTIFY
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'⏳Стирка {settings.washing_time} мин.',
                    callback_data=CallbackData.EDIT_WASHING_TIME
                ),
                InlineKeyboardButton(
                    text=f'💨Сушка {settings.drying_time} мин.',
                    callback_data=CallbackData.EDIT_DRYING_TIME
                )
            ],
            [go_to_main_menu_button]
        ]
    )


choose_grade_keyboard = InlineKeyboardBuilder().add(
    *[
        InlineKeyboardButton(
            text=f'{grade_letter}',
            callback_data=CallbackData.CHANGE_GRADE_TO_ + grade_letter
        )
        for grade_letter in GRADES
    ],
    InlineKeyboardButton(
        text=f'⏪Настройки',
        callback_data=CallbackData.OPEN_SETTINGS
    ),
    InlineKeyboardButton(
        text=f'❓Сбросить класс',
        callback_data=CallbackData.CHANGE_GRADE_TO_ + 'None'
    )
).adjust(3, 3, 2).as_markup()
