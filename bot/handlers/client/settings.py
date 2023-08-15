from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.db_funcs import Repository
from bot.filters import SaveUser
from bot.funcs.settings import (
    edit_bool_settings_func, edit_grade_setting_func,
    edit_laundry_time_func,
)
from bot.keyboards import (
    cancel_state_keyboard, settings_keyboard,
    choose_grade_keyboard,
)
from bot.utils.consts import (
    CallbackData, SlashCommands, TextCommands,
    times_eng_to_ru,
)
from bot.utils.states import EditingSettings


router = Router(name=__name__)

settings_welcome_text = """
Привет! Я - настройки!

*Класс* - твой класс.
*Уроки* - уведомления при изменении расписания.
*Новости* - уведомления о мероприятиях, новостях.
*Стирка* - время таймера для стирки.
*Сушка* - время таймера для сушки.
""".strip()


@router.message(F.text == TextCommands.SETTINGS, SaveUser())
@router.message(Command(SlashCommands.SETTINGS), SaveUser())
@router.callback_query(F.data == CallbackData.OPEN_SETTINGS, SaveUser())
async def open_settings_handler(
        callback: types.CallbackQuery | types.Message,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки "Настройки".
    """
    settings = await repo.get_settings(callback.from_user.id)
    keyboard = await settings_keyboard(settings)

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_text(
            text=settings_welcome_text,
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text=settings_welcome_text,
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith(CallbackData.PREFIX_SWITCH))
async def edit_bool_settings_handler(
        callback: types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик кнопок уведомлений "Уроки" и "Новости".
    """
    await edit_bool_settings_func(repo, callback.from_user.id, callback.data)

    settings = await repo.get_settings(callback.from_user.id)
    keyboard = await settings_keyboard(settings)

    await callback.message.edit_text(
        text=settings_welcome_text,
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith(CallbackData.CHANGE_GRADE_TO_))
async def edit_grade_settings_handler(
        callback: types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик кнопок изменения класса.
    """
    change = await edit_grade_setting_func(
        repo, callback.from_user.id, callback.data
    )

    if change:
        await open_settings_handler(callback, repo)
    else:
        await callback.message.edit_text(
            text=settings_welcome_text,
            reply_markup=choose_grade_keyboard
        )


@router.callback_query(F.data.startswith(CallbackData.EDIT_SETTINGS_PREFIX))
async def edit_laundry_start_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик кнопок изменения времени таймера прачки.
    """
    attr = callback.data.replace(CallbackData.EDIT_SETTINGS_PREFIX, '')

    await state.set_state(EditingSettings.writing)
    await state.update_data(
        start_id=callback.message.message_id,
        attr=attr
    )

    text = f'🕛Введите `{times_eng_to_ru[attr]}` в минутах (целых)'
    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(StateFilter(EditingSettings.writing))
async def edit_laundry_time_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
) -> None:
    """
    Обработчик сообщения с минутами для изменения таймера прачки.
    """
    data = await state.get_data()
    start_id = data['start_id']
    attr = data['attr']

    result = await edit_laundry_time_func(
        repo, message.from_user.id, attr, message.text
    )

    if result:
        text = f'✅`{times_eng_to_ru[attr].capitalize()}` ' \
               f'установлено на `{result}` минут.'
        settings = await repo.get_settings(message.from_user.id)
        keyboard = await settings_keyboard(settings)
        await state.clear()
    else:
        text = f'❌Не распознал `{message.text}` как минуты. Попробуй ещё раз.'
        keyboard = cancel_state_keyboard

    await message.bot.edit_message_text(
        text=text,
        reply_markup=keyboard,
        message_id=start_id,
        chat_id=message.chat.id
    )
    await message.delete()
