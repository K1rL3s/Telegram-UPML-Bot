from io import BytesIO

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.database.db_funcs import edit_meal_by_date
from src.handlers.admin import get_meal_by_date, load_lessons_handler
from src.keyboards import (
    cancel_state_keyboard,
    confirm_edit_menu_keyboard, start_menu_keyboard,
    choose_meal_keyboard,
    admin_panel_keyboard,
)
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.consts import CallbackData, menu_eng_to_ru
from src.utils.datehelp import date_by_format, date_today, format_date
from src.utils.decorators import admin_required
from src.utils.states import LoadingLessons, EditingMenu
from src.utils.throttling import rate_limit


@admin_required
async def auto_update_cafe_menu_view(
        callback: types.CallbackQuery, *_, **__
) -> None:
    """
    Обработчик кнопки "Загрузить меню",
    загружает и обрабатывает PDF расписание еды с сайта лицея.
    """
    status, text = await save_cafe_menu()

    await callback.message.edit_text(
        text=text,
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )


@admin_required
async def edit_cafe_menu_start_view(
        callback: types.CallbackQuery, *_, **__
) -> None:
    """
    Обрабочтки кнопки "Изменить меню".
    """
    text = f"""
Введите дату дня, меню которого хотите изменить в формате *ДД.ММ.ГГГГ*
Например, *{format_date(date_today())}*
""".strip()

    await EditingMenu.choose_date.set()
    await Dispatcher.get_current().current_state().set_data(
        {
            "start_id": callback.message.message_id
        }
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@admin_required
async def edit_cafe_menu_date_view(
        message: types.Message, state: FSMContext, *_, **__
) -> None:
    """
    Обработчик ввода доты для изменения меню.
    """
    try:
        edit_menu_date = date_by_format(message.text)
    except ValueError:
        text = f'Не удалось понять дату "`{message.text}`", попробуйте ещё раз'
        keyboard = cancel_state_keyboard
    else:
        text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
               f'Какой приём пищи вы хотите изменить?'
        keyboard = choose_meal_keyboard
        await EditingMenu.next()
        async with state.proxy() as data:
            data['edit_menu_date'] = edit_menu_date

    async with state.proxy() as data:
        start_id = data['start_id']

    await Bot.get_current().edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=keyboard
    )

    await message.delete()  # ?


@admin_required
async def edit_cafe_menu_meal_view(
        callback: types.CallbackQuery, state: FSMContext, *_, **__
) -> None:
    """
    Обработчик кнопки с выбором приёма пищи для изменения.
    """
    edit_meal = callback.data.split("_")[-1]
    async with state.proxy() as data:
        edit_menu_date = data['edit_menu_date']
        data['edit_meal'] = edit_meal

    text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
           f'*Приём пищи*: `{menu_eng_to_ru[edit_meal].capitalize()}`\n' \
           f'*Меню*:\n' \
           f'```\n{get_meal_by_date(edit_meal, edit_menu_date)}```\n\n' \
           'Чтобы изменить, отправьте *одним сообщением* изменённую версию.'

    await EditingMenu.next()

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@admin_required
async def edit_cafe_menu_text_view(
        message: types.Message,
        state: FSMContext, *_, **__
) -> None:
    """
    Обработчик сообщения с изменённой версией приёма пищи.
    """
    new_menu = message.text
    async with state.proxy() as data:
        start_id = data['start_id']
        edit_menu_date = data['edit_menu_date']
        edit_meal = data['edit_meal']
        data['new_menu'] = new_menu
        # Можно в одну строку, но пичарм жалуется
        new_menu_ids = data.get('new_menu_ids', [])
        new_menu_ids.append(message.message_id)
        data['new_menu_ids'] = new_menu_ids

    text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
           f'*Приём пищи*: `{menu_eng_to_ru[edit_meal].capitalize()}`\n' \
           f'*Новое меню*:\n```\n{new_menu}```\n\n' \
           'Для сохранения нажмите кнопку. Если хотите изменить, ' \
           'отправьте сообщение повторно.'

    await Bot.get_current().edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_edit_menu_keyboard
    )


@admin_required
async def edit_cafe_menu_confirm_view(
        callback: types.CallbackQuery, state: FSMContext, *_, **__
) -> None:
    """
    Обработчик подтверждения изменения меню.
    """
    async with state.proxy() as data:
        edit_menu_date = data['edit_menu_date']
        edit_meal = data['edit_meal']
        new_menu = data['new_menu']
        new_menu_ids = data['new_menu_ids']
    await state.finish()

    edit_meal_by_date(
        edit_meal, new_menu, edit_menu_date, callback.from_user.id
    )

    text = f'*{menu_eng_to_ru[edit_meal].capitalize()}* на ' \
           f'*{format_date(edit_menu_date)}* успешно изменён!'

    await callback.message.edit_text(
        text=text,
        reply_markup=admin_panel_keyboard(callback.from_user.id)
    )

    for new_menu_id in new_menu_ids:
        await Bot.get_current().delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_menu_id
        )


@admin_required
async def start_load_lessons_view(
        callback: types.CallbackQuery, *_, **__
) -> None:
    """
    Обработчик кнопки "Загрузить уроки".
    """
    await LoadingLessons.image.set()
    text = 'Отправьте изображение(-я) расписания уроков'

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@rate_limit(0)
@admin_required
async def load_lessons_view(
        message: types.Message, state: FSMContext, *_, **__
) -> None:
    """
    Обработчик сообщений с изображениями
    после нажатия кнопки "Загрузить уроки".
    """
    await message.photo[-1].download(destination_file=(image := BytesIO()))

    text = await load_lessons_handler(message.chat.id, image)

    if state:
        await state.finish()

    if isinstance(text, str):
        await message.reply(
            text=text,
            reply_markup=start_menu_keyboard
        )
        return

    grade, lessons_date = text
    text = f'Расписание для *{grade}-х классов* на ' \
           f'*{format_date(lessons_date)}* сохранено!'

    await message.reply(
        text=text,
        reply_markup=start_menu_keyboard
    )


def register_admin_updates_view(dp: Dispatcher):
    dp.register_callback_query_handler(
        auto_update_cafe_menu_view,
        text=CallbackData.AUTO_UPDATE_CAFE_MENU
    )
    dp.register_callback_query_handler(
        start_load_lessons_view,
        text=CallbackData.UPLOAD_LESSONS
    )
    dp.register_message_handler(
        load_lessons_view,
        content_types=['photo'],
        state=LoadingLessons.image
    )

    dp.register_callback_query_handler(
        edit_cafe_menu_start_view,
        text=CallbackData.EDIT_CAFE_MENU
    )
    dp.register_message_handler(
        edit_cafe_menu_date_view,
        state=EditingMenu.choose_date
    )
    dp.register_callback_query_handler(
        edit_cafe_menu_meal_view,
        state=EditingMenu.choose_meal
    )
    dp.register_message_handler(
        edit_cafe_menu_text_view,
        state=EditingMenu.editing
    )
    dp.register_callback_query_handler(
        edit_cafe_menu_confirm_view,
        state=EditingMenu.editing
    )
