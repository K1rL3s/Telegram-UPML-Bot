from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command, StateFilter

from bot.callbacks import OpenMenu, SettingsData
from bot.funcs.client.settings import (
    edit_bool_settings_func,
    edit_grade_setting_func,
    edit_laundry_time_func,
)
from bot.keyboards import (
    cancel_state_keyboard,
    choose_grade_keyboard,
    settings_keyboard,
)
from bot.middlewares.inner.save_user import SaveUpdateUserMiddleware
from bot.utils.enums import Actions, Menus, SlashCommands, TextCommands, UserCallback
from bot.utils.phrases import SETTINGS_WELCOME_TEXT
from bot.utils.states import EditingSettings

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)
router.message.middleware(SaveUpdateUserMiddleware())


@router.callback_query(OpenMenu.filter(F.menu == Menus.SETTINGS))
async def settings_callback_handler(
    callback: "CallbackQuery",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Настройки"."""
    keyboard = await settings_keyboard(repo.settings, callback.from_user.id)

    await callback.message.edit_text(
        text=SETTINGS_WELCOME_TEXT,
        reply_markup=keyboard,
    )


@router.message(F.text == TextCommands.SETTINGS)
@router.message(Command(SlashCommands.SETTINGS))
async def settings_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/settings"."""
    keyboard = await settings_keyboard(repo.settings, message.from_user.id)

    await message.answer(text=SETTINGS_WELCOME_TEXT, reply_markup=keyboard)


@router.callback_query(SettingsData.filter(F.action == Actions.SWITCH))
async def edit_bool_settings_handler(
    callback: "CallbackQuery",
    callback_data: "SettingsData",
    repo: "Repository",
) -> None:
    """Обработчик кнопок уведомлений "Уроки" и "Новости"."""
    await edit_bool_settings_func(
        repo.settings,
        callback.from_user.id,
        callback_data.attr,
    )

    keyboard = await settings_keyboard(repo.settings, callback.from_user.id)

    await callback.message.edit_text(text=SETTINGS_WELCOME_TEXT, reply_markup=keyboard)


@router.callback_query(SettingsData.filter(F.action == UserCallback.CHANGE_GRADE))
async def edit_grade_settings_handler(
    callback: "CallbackQuery",
    callback_data: "SettingsData",
    repo: "Repository",
) -> None:
    """Обработчик кнопок изменения (выбора) класса."""
    change = await edit_grade_setting_func(
        repo.settings,
        callback.from_user.id,
        callback_data.attr,
    )

    if change:
        await settings_callback_handler(callback, repo)
    else:
        await callback.message.edit_text(
            text=SETTINGS_WELCOME_TEXT,
            reply_markup=choose_grade_keyboard,
        )


@router.callback_query(SettingsData.filter(F.action == Actions.EDIT))
async def edit_laundry_start_handler(
    callback: "CallbackQuery",
    callback_data: "SettingsData",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок изменения времени таймера прачечной."""
    await state.set_state(EditingSettings.writing)
    await state.update_data(
        start_id=callback.message.message_id,
        attr=callback_data.attr,
    )

    text = (
        "🕛 Чтобы установить таймер на срабатывание через какое-то время, "
        "введите часы и минуты через точку, запятую или пробел "
        "<i>(0.30, 1 0, 12,45)</i>.\n"
        "⏰ Чтобы установить таймер на срабатывание в какое-то время, "
        "введите это время через двоеточие <i>(12:30, 16:00, 19:50)</i>"
    )
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingSettings.writing))
async def edit_laundry_time_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик сообщения с минутами для изменения таймера прачечной."""
    data = await state.get_data()
    start_id: int = data["start_id"]
    attr: str = data["attr"]

    text, keyboard = await edit_laundry_time_func(
        message.from_user.id,
        attr,
        message.text,
        state,
        repo.settings,
    )

    await message.delete()
    await message.bot.edit_message_text(
        text=text,
        reply_markup=keyboard,
        message_id=start_id,
        chat_id=message.chat.id,
    )
