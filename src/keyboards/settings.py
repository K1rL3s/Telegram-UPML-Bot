from aiogram.types.inline_keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.database.db_funcs import get_settings
from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData, GRADES


def settings_keyboard(
        user_id: int
) -> InlineKeyboardMarkup:
    settings = get_settings(user_id)

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            'Класс ' + (settings.class_ if settings.class_ else '❓'),
            callback_data=CallbackData.CHANGE_GRADE_TO_
        ),
        InlineKeyboardButton(
            'Уроки ' + ('✅' if settings.lessons_notify else '❌'),
            callback_data=CallbackData.SWITCH_LESSONS_NOTIFY
        ),
        InlineKeyboardButton(
            'Новости ' + ('✅' if settings.news_notify else '❌'),
            callback_data=CallbackData.SWITCH_NEWS_NOTIFY
        )
    ).add(
        InlineKeyboardButton(
            f'⏳Стирка {settings.washing_time} мин.',
            callback_data=CallbackData.EDIT_WASHING_TIME
        ),
        InlineKeyboardButton(
            f'💨Сушка {settings.drying_time} мин.',
            callback_data=CallbackData.EDIT_DRYING_TIME
        )
    ).add(
        go_to_main_menu_button
    )


choose_grade_keyboard = InlineKeyboardMarkup(row_width=3)
for grade_letter in GRADES:
    choose_grade_keyboard.insert(
        InlineKeyboardButton(
            f'{grade_letter}',
            callback_data=CallbackData.CHANGE_GRADE_TO_ + grade_letter
        )
    )

choose_grade_keyboard.row(
    InlineKeyboardButton(
        f'⏪Настройки',
        callback_data=CallbackData.OPEN_SETTINGS
    ),
    InlineKeyboardButton(
        f'❓Сбросить класс',
        callback_data=CallbackData.CHANGE_GRADE_TO_ + 'None'
    ),
)
