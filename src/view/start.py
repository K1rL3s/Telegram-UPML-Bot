from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.keyboards import (
    go_to_main_menu_keyboard, main_menu_keyboard, admin_panel_keyboard,
)
from src.utils.consts import CallbackData
from src.utils.decorators import admin_required, save_new_user_decor


@save_new_user_decor
async def start_view(message: types.Message) -> None:
    """
    Обработчик команды "/start".
    """
    text = 'Привет! Я - стартовое меню.'

    await message.reply(
        text=text,
        reply_markup=go_to_main_menu_keyboard
    )


@save_new_user_decor
async def main_menu_view(message: types.Message | types.CallbackQuery) -> None:
    """
    Обработчик команды "/menu" и кнопки "Главное меню".
    """
    text = 'Привет! Я - главное меню.'
    keyboard = main_menu_keyboard(message.from_user.id)

    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    else:
        await message.reply(
            text=text,
            reply_markup=keyboard
        )


@admin_required
async def admin_panel_view(callback: types.CallbackQuery, *_, **__) -> None:
    """
    Обработчик кнопки "Админ панель".
    """
    text = """
Привет! Я - админ панель.

*Загрузить меню* - автоматическое обновление еды информацией с сайта лицея.
*Изменить меню* - ручное изменение еды.
*Загрузить уроки* - ручная загрузка изображений с расписанием уроков.
*Уведомление* - сделать оповещение.
""".strip()
    keyboard = admin_panel_keyboard(callback.from_user.id)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def cancel_state(
        message: types.Message | types.CallbackQuery,
        state: FSMContext
) -> None:
    """
    Обработчик кнопок с отменой состояний и команд "/cancel", "/stop".
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await main_menu_view(message)


def register_start_view(dp: Dispatcher):
    dp.register_message_handler(
        cancel_state,
        commands=['cancel', 'stop'],
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_state,
        text=CallbackData.CANCEL_STATE,
        state='*'
    )
    dp.register_message_handler(
        start_view,
        commands=['start'],
    )
    dp.register_message_handler(
        main_menu_view,
        commands=['menu'],
    )
    dp.register_callback_query_handler(
        main_menu_view,
        text=CallbackData.OPEN_MAIN_MENU
    )
    dp.register_callback_query_handler(
        admin_panel_view,
        text=CallbackData.OPEN_ADMIN_PANEL
    )
