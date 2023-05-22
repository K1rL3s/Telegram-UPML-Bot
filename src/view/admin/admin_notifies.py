from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.handlers.admin import do_notifies, get_users_for_notify
from src.keyboards import (
    cancel_state_keyboard, notify_panel_keyboard, notify_for_grade_keyboard,
    notify_for_class_keyboard, admin_panel_keyboard, notify_confirm_keyboard,
)
from src.utils.consts import CallbackData, notifies_eng_to_ru
from src.utils.decorators import admin_required
from src.utils.states import DoNotify


@admin_required
async def notify_panel_view(callback: types.CallbackQuery, *_, **__) -> None:
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


@admin_required
async def notify_for_who_view(callback: types.CallbackQuery, *_, **__) -> None:
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
        await DoNotify.writing.set()
        await Dispatcher.get_current().current_state().set_data(
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


@admin_required
async def notify_message_view(
        message: types.Message, state: FSMContext, *_, **__
) -> None:
    async with state.proxy() as data:
        start_id = data['start_id']
        notify_type = data['notify_type']
        data['message_text'] = message.text
        # можно в одну строку, но пичарм жалуется
        messages_ids = data.get('messages_ids', [])
        messages_ids.append(message.message_id)
        data['messages_ids'] = messages_ids

    text = f'Тип: `{notifies_eng_to_ru.get(notify_type, notify_type)}`\n' \
           f'Сообщение:\n```\n{message.text}```\n\n' \
           'Для отправки нажмите кнопку. Если хотите изменить, ' \
           'отправьте сообщение повторно.'

    await Bot.get_current().edit_message_text(
        text=text,
        message_id=start_id,
        chat_id=message.chat.id,
        reply_markup=notify_confirm_keyboard
    )


@admin_required
async def notify_confirm_view(
        callback: types.CallbackQuery, state: FSMContext, *_, **__
) -> None:
    async with state.proxy() as data:
        notify_type = data['notify_type']
        message_text = data['message_text']
        messages_ids = data['messages_ids']
    await state.finish()

    users = get_users_for_notify(notify_type, is_news=True)
    await do_notifies(
        message_text, users, callback.from_user.id,
        notifies_eng_to_ru.get(notify_type, notify_type)
    )

    text = 'Рассылка завершена!'
    await callback.message.edit_text(
        text=text,
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )

    for message_id in messages_ids:
        await Bot.get_current().delete_message(
            chat_id=callback.message.chat.id,
            message_id=message_id
        )


def register_admin_notifies_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        notify_panel_view,
        text=CallbackData.DO_A_NOTIFY_FOR_
    )
    dp.register_callback_query_handler(
        notify_for_who_view,
        lambda callback: callback.data.startswith(
            CallbackData.DO_A_NOTIFY_FOR_
        )
    )
    dp.register_message_handler(
        notify_message_view,
        state=DoNotify.writing
    )
    dp.register_callback_query_handler(
        notify_confirm_view,
        state=DoNotify.writing,
        text=CallbackData.NOTIFY_CONFIRM
    )
