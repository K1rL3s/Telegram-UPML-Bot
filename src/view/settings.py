from aiogram import Dispatcher, types

from src.handlers.settings import (
    edit_bool_settings_handler,
    edit_grade_setting_handler, open_settings_handler,
)
from src.keyboards import settings_keyboard, choose_grade_keyboard
from src.utils.consts import CallbackData
from src.utils.decorators import save_new_user_decor
from src.utils.funcs import extract_username


settings_welcome_text = """
Привет! Я - настройки!

*Класс* - твой класс.
*Расписание* - уведомления при изменении расписания.
*Новости* - уведомления о мероприятиях, новостях.
    """.strip()


@save_new_user_decor
async def open_settings_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Настройки".
    """
    grade, letter, lessons_notify, news_notify = open_settings_handler(
        callback.from_user.id, extract_username(callback)
    )

    keyboard = settings_keyboard(
        grade=grade,
        letter=letter,
        lessons_notify=lessons_notify,
        news_notify=news_notify
    )

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


async def edit_bool_settings_view(callback: types.CallbackQuery):
    grade, letter, lessons_notify, news_notify = edit_bool_settings_handler(
        callback.from_user.id, callback.data
    )

    keyboard = settings_keyboard(
        grade=grade,
        letter=letter,
        lessons_notify=lessons_notify,
        news_notify=news_notify,
    )

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


async def edit_grade_settings_view(callback: types.CallbackQuery):
    values = edit_grade_setting_handler(callback.from_user.id, callback.data)

    if values is None:
        await callback.message.edit_text(
            text=settings_welcome_text,
            reply_markup=choose_grade_keyboard
        )
        return

    grade, letter, lessons_notify, news_notify = values

    keyboard = settings_keyboard(
        grade=grade,
        letter=letter,
        lessons_notify=lessons_notify,
        news_notify=news_notify,
    )

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


def register_setings_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        open_settings_view,
        text=CallbackData.OPEN_SETTINGS
    )
    dp.register_callback_query_handler(
        edit_bool_settings_view,
        lambda callback: callback.data.startswith(CallbackData.PREFIX_SWITCH)
    )
    dp.register_callback_query_handler(
        edit_grade_settings_view,
        lambda callback: callback.data.startswith(
            CallbackData.CHANGE_GRADE_TO_
        )
    )
