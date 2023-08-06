from io import BytesIO

from aiogram import F, Router, types
from aiogram.filters import StateFilter

from aiogram.fsm.context import FSMContext

from src.database.db_funcs import edit_meal_by_date
from src.handlers.admin import get_meal_by_date, load_lessons_handler
from src.keyboards import (
    cancel_state_keyboard,
    confirm_edit_menu_keyboard, go_to_main_menu_keyboard,
    choose_meal_keyboard,
    admin_panel_keyboard,
)
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.consts import CallbackData, menu_eng_to_ru
from src.utils.datehelp import date_by_format, date_today, format_date
from src.utils.decorators import admin_required
from src.utils.states import LoadingLessons, EditingMenu
from src.utils.throttling import rate_limit


router = Router(name='admin_updates')


@router.callback_query(F.data == CallbackData.AUTO_UPDATE_CAFE_MENU)
@admin_required
async def auto_update_cafe_menu_view(
        callback: types.CallbackQuery, **_
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


@router.callback_query(F.data == CallbackData.EDIT_CAFE_MENU)
@admin_required
async def edit_cafe_menu_start_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обрабочтки кнопки "Изменить меню".
    """
    text = f"""
Введите дату дня, меню которого хотите изменить в формате *ДД.ММ.ГГГГ*
Например, `{format_date(date_today())}`
""".strip()

    await state.set_state(EditingMenu.choose_date)
    await state.set_data({"start_id": callback.message.message_id})

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(StateFilter(EditingMenu.choose_date))
@admin_required
async def edit_cafe_menu_date_view(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Обработчик ввода доты для изменения меню.
    """
    edit_menu_date = date_by_format(message.text)
    if not edit_menu_date:  # is False
        text = f'Не удалось понять дату "`{message.text}`", попробуйте ещё раз'
        keyboard = cancel_state_keyboard
    else:
        text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
               f'Какой приём пищи вы хотите изменить?'
        keyboard = choose_meal_keyboard
        await state.set_state(EditingMenu.choose_meal)
        await state.update_data(edit_menu_date=edit_menu_date)

    start_id = (await state.get_data())['start_id']

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=keyboard
    )

    await message.delete()  # ?


@router.callback_query(StateFilter(EditingMenu.choose_meal))
@admin_required
async def edit_cafe_menu_meal_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик кнопки с выбором приёма пищи для изменения.
    """
    edit_meal = callback.data.split("_")[-1]
    edit_menu_date = (await state.get_data())['edit_menu_date']
    await state.update_data(edit_meal=edit_meal)

    text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
           f'*Приём пищи*: `{menu_eng_to_ru[edit_meal].capitalize()}`\n' \
           f'*Меню*:\n' \
           f'```\n' \
           f'{get_meal_by_date(edit_meal, edit_menu_date) or "Н/д"}' \
           f'```\n\n' \
           'Чтобы изменить, отправьте *одним сообщением* изменённую версию.'

    await state.set_state(EditingMenu.writing)

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(StateFilter(EditingMenu.writing))
@admin_required
async def edit_cafe_menu_text_view(
        message: types.Message,
        state: FSMContext,
) -> None:
    """
    Обработчик сообщения с изменённой версией приёма пищи.
    """
    data = await state.get_data()
    start_id = data['start_id']
    edit_menu_date = data['edit_menu_date']
    edit_meal = data['edit_meal']

    new_menu = message.text
    new_menu_ids = data.get('new_menu_ids', [])
    new_menu_ids.append(message.message_id)
    await state.update_data(new_menu=new_menu, new_menu_ids=new_menu_ids)

    text = f'*Дата*: `{format_date(edit_menu_date)}`\n' \
           f'*Приём пищи*: `{menu_eng_to_ru[edit_meal].capitalize()}`\n' \
           f'*Новое меню*:\n```\n{new_menu}```\n\n' \
           'Для сохранения нажмите кнопку. Если хотите изменить, ' \
           'отправьте сообщение повторно.'

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_edit_menu_keyboard
    )


@router.callback_query(StateFilter(EditingMenu.writing))
@admin_required
async def edit_cafe_menu_confirm_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик подтверждения изменения меню.
    """
    data = await state.get_data()
    edit_menu_date = data['edit_menu_date']
    edit_meal = data['edit_meal']
    new_menu = data['new_menu']
    new_menu_ids = data['new_menu_ids']

    await state.clear()

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
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_menu_id
        )


@router.callback_query(F.data == CallbackData.UPLOAD_LESSONS)
@admin_required
async def start_load_lessons_view(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик кнопки "Загрузить уроки".
    """
    await state.set_state(LoadingLessons.image)
    text = 'Отправьте изображение(-я) расписания уроков'

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(StateFilter(LoadingLessons.image), F.content_type == 'photo')
@rate_limit(0)
@admin_required
async def load_lessons_view(
        message: types.Message,
        state: FSMContext,
) -> None:
    """
    Обработчик сообщений с изображениями
    после нажатия кнопки "Загрузить уроки".
    """
    file_id = message.photo[-1].file_id
    file = await message.bot.get_file(file_id)
    await message.bot.download_file(file.file_path, image := BytesIO())

    result = await load_lessons_handler(message.chat.id, image, message.bot)

    if state:
        await state.clear()

    if isinstance(result, str):
        await message.reply(
            text=result,
            reply_markup=go_to_main_menu_keyboard
        )
        return

    grade, lessons_date = result
    text = f'Расписание для *{grade}-х классов* на ' \
           f'*{format_date(lessons_date)}* сохранено!'

    await message.reply(
        text=text,
        reply_markup=go_to_main_menu_keyboard
    )
