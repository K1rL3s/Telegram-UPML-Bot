from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.database.db_funcs import get_settings
from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData, GRADES


def settings_keyboard(
        user_id: int
) -> InlineKeyboardMarkup:
    settings = get_settings(user_id)

    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text='Класс ' + (settings.class_ if settings.class_ else '❓'),
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
    ).add(
        InlineKeyboardButton(
            text=f'⏳Стирка {settings.washing_time} мин.',
            callback_data=CallbackData.EDIT_WASHING_TIME
        ),
        InlineKeyboardButton(
            text=f'💨Сушка {settings.drying_time} мин.',
            callback_data=CallbackData.EDIT_DRYING_TIME
        )
    ).add(
        go_to_main_menu_button
    ).as_markup()


choose_grade_keyboard = InlineKeyboardBuilder()
for grade_letter in GRADES:
    choose_grade_keyboard.add(
        InlineKeyboardButton(
            text=f'{grade_letter}',
            callback_data=CallbackData.CHANGE_GRADE_TO_ + grade_letter
        )
    )

choose_grade_keyboard.row(
    InlineKeyboardButton(
        text=f'⏪Настройки',
        callback_data=CallbackData.OPEN_SETTINGS
    ),
    InlineKeyboardButton(
        text=f'❓Сбросить класс',
        callback_data=CallbackData.CHANGE_GRADE_TO_ + 'None'
    ),
)

choose_grade_keyboard = choose_grade_keyboard.as_markup()
