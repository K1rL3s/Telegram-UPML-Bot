from aiogram.types.inline_keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData, GRADES


def settings_keyboard(
        grade: str = None,
        letter: str = None,
        lessons_notify: bool = False,
        news_notify: bool = False
) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            'Класс ' + (f'{grade}{letter}' if (grade and letter) else '❓'),
            callback_data=CallbackData.CHANGE_GRADE_TO_
        ),
        InlineKeyboardButton(
            'Расписание ' + ('✅' if lessons_notify else '❌'),
            callback_data=CallbackData.SWITCH_LESSONS_NOTIFY
        ),
        InlineKeyboardButton(
            'Новости ' + ('✅' if news_notify else '❌'),
            callback_data=CallbackData.SWITCH_NEWS_NOTIFY
        )
    ).row(
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
