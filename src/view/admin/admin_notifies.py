from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.handlers.admin import do_notifies, get_users_for_notify
from src.keyboards import (
    cancel_state_keyboard, notify_panel_keyboard, notify_for_grade_keyboard,
    notify_for_class_keyboard, admin_panel_keyboard, notify_confirm_keyboard,
)
from src.utils.consts import CallbackData, notifies_eng_to_ru
from src.utils.decorators import admin_required
from src.utils.states import DoNotify


router = Router(name='admin_notifies')


@router.callback_query(F.data == CallbackData.DO_A_NOTIFY_FOR_)
@admin_required
async def notify_panel_view(callback: types.CallbackQuery, **_) -> None:
    """
    Обработчик кнопки "Уведомление".
    """
    text = """
Привет! Я - панель уведомлений.

*Всем* - для всех пользователей.
*Поток* - для 10 или 11 классов.
*Класс* - для конкретного класса.
""".strip()

    await callback.message.edit_text(
        text=text,
        reply_markup=notify_panel_keyboard
    )


@router.callback_query(F.data.startswith(CallbackData.DO_A_NOTIFY_FOR_))
@admin_required
async def notify_for_who_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик нажатия одной из кнопок уведомления в панели уведомлений.
    """
    notify_type = callback.data.replace(CallbackData.DO_A_NOTIFY_FOR_, '')

    if callback.data == CallbackData.FOR_GRADE:
        text = 'Выберите, каким классам сделать уведомление'
        keyboard = notify_for_grade_keyboard
    elif callback.data == CallbackData.FOR_CLASS:
        text = 'Выберите, какому классу сделать уведомление'
        keyboard = notify_for_class_keyboard
    else:
        await state.set_state(DoNotify.writing)
        await state.set_data(
            {
                "start_id": callback.message.message_id,
                # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
                "notify_type": notify_type,
            }
        )
        text = f'Тип: `{notifies_eng_to_ru.get(notify_type, notify_type)}`\n' \
               'Напишите сообщение, которое будет в уведомлении'
        keyboard = cancel_state_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.message(StateFilter(DoNotify.writing))
@admin_required
async def notify_message_view(
        message: types.Message,
        state: FSMContext,
) -> None:
    data = await state.get_data()
    start_id = data['start_id']
    notify_type = data['notify_type']

    messages_ids = data.get('messages_ids', [])
    messages_ids.append(message.message_id)
    await state.update_data(
        message_text=message.text,
        messages_ids=messages_ids
    )

    text = f'Тип: `{notifies_eng_to_ru.get(notify_type, notify_type)}`\n' \
           f'Сообщение:\n```\n{message.text}```\n\n' \
           'Для отправки нажмите кнопку. Если хотите изменить, ' \
           'отправьте сообщение повторно.'

    await message.bot.edit_message_text(
        text=text,
        message_id=start_id,
        chat_id=message.chat.id,
        reply_markup=notify_confirm_keyboard
    )


@router.callback_query(
    F.data == CallbackData.NOTIFY_CONFIRM,
    StateFilter(DoNotify.writing)
)
@admin_required
async def notify_confirm_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    data = await state.get_data()
    notify_type = data['notify_type']
    message_text = data['message_text']
    messages_ids = data['messages_ids']
    await state.clear()

    users = get_users_for_notify(notify_type, is_news=True)
    await do_notifies(
        callback.bot, message_text, users, callback.from_user.id,
        notifies_eng_to_ru.get(notify_type, notify_type)
    )

    text = 'Рассылка завершена!'
    await callback.message.edit_text(
        text=text,
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )

    for message_id in messages_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=message_id
        )
