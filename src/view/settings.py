from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.handlers.settings import (
    edit_bool_settings_handler, edit_grade_setting_handler,
    edit_laundry_time_handler,
)
from src.keyboards import (
    cancel_state_keyboard, settings_keyboard,
    choose_grade_keyboard,
)
from src.utils.consts import CallbackData, times_eng_to_ru
from src.utils.decorators import save_new_user_decor
from src.utils.states import EditingSettings


settings_welcome_text = """
Привет! Я - настройки!

*Класс* - твой класс.
*Уроки* - уведомления при изменении расписания.
*Новости* - уведомления о мероприятиях, новостях.
*Стирка* - время таймера для стирки.
*Сушка* - время таймера для сушки.
""".strip()


@save_new_user_decor
async def open_settings_view(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки "Настройки".
    """
    keyboard = settings_keyboard(callback.from_user.id)

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


async def edit_bool_settings_view(callback: types.CallbackQuery):
    edit_bool_settings_handler(callback.from_user.id, callback.data)

    keyboard = settings_keyboard(callback.from_user.id)

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


async def edit_grade_settings_view(callback: types.CallbackQuery):
    settings = edit_grade_setting_handler(callback.from_user.id, callback.data)

    if settings is None:
        await callback.message.edit_text(
            text=settings_welcome_text,
            reply_markup=choose_grade_keyboard
        )
        return

    keyboard = settings_keyboard(callback.from_user.id)

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


async def edit_laundry_start_view(callback: types.CallbackQuery) -> None:
    attr = callback.data.replace(CallbackData.EDIT_SETTINGS_PREFIX, '')

    await EditingSettings.writing.set()
    await Dispatcher.get_current().current_state().set_data(
        {
            "start_id": callback.message.message_id,
            "attr": attr,
        }
    )

    text = f'🕛Введите `{times_eng_to_ru[attr]}` в минутах'
    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


async def edit_laundry_time_view(
        message: types.Message, state: FSMContext
) -> None:
    async with state.proxy() as data:
        start_id = data['start_id']
        attr = data['attr']

    result = edit_laundry_time_handler(
        message.from_user.id, attr, message.text
    )

    if result:
        text = f'✅`{times_eng_to_ru[attr].capitalize()}` ' \
               f'установлено на `{result}` минут.'
        keyboard = settings_keyboard(message.from_user.id)
        await state.finish()
    else:
        text = f'❌Не распознал `{message.text}` как минуты. Попробуй ещё раз.'
        keyboard = cancel_state_keyboard

    await Bot.get_current().edit_message_text(
        text=text,
        reply_markup=keyboard,
        message_id=start_id,
        chat_id=message.chat.id
    )
    await message.delete()


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
    dp.register_callback_query_handler(
        edit_laundry_start_view,
        lambda callback: callback.data.startswith(
            CallbackData.EDIT_SETTINGS_PREFIX
        )
    )
    dp.register_message_handler(
        edit_laundry_time_view,
        state=EditingSettings.writing
    )
