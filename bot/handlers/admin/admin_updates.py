from datetime import date
from io import BytesIO

from aiogram import F, Router, types
from aiogram.filters import StateFilter

from aiogram.fsm.context import FSMContext

from bot.custom_types import Album
from bot.database.db_funcs import Repository
from bot.filters import IsAdmin
from bot.funcs.admin import get_meal_by_date, load_lessons_func
from bot.keyboards import (
    cancel_state_keyboard,
    confirm_edit_menu_keyboard, go_to_main_menu_keyboard,
    choose_meal_keyboard,
    admin_panel_keyboard,
)
from bot.upml.save_cafe_menu import save_cafe_menu
from bot.utils.consts import CallbackData, menu_eng_to_ru
from bot.utils.datehelp import date_by_format, date_today, format_date
from bot.utils.states import LoadingLessons, EditingMenu


router = Router(name=__name__)


@router.callback_query(F.data == CallbackData.AUTO_UPDATE_CAFE_MENU, IsAdmin())
async def auto_update_cafe_menu_handler(
        callback: types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки "Загрузить меню",
    загружает и обрабатывает PDF расписание еды с сайта лицея.
    """
    status, text = await save_cafe_menu(repo)

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo, callback.from_user.id)
    )


@router.callback_query(F.data == CallbackData.EDIT_CAFE_MENU, IsAdmin())
async def edit_cafe_menu_start_handler(
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


@router.message(StateFilter(EditingMenu.choose_date), IsAdmin())
async def edit_cafe_menu_date_handler(
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


@router.callback_query(StateFilter(EditingMenu.choose_meal), IsAdmin())
async def edit_cafe_menu_meal_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки с выбором приёма пищи для изменения.
    """
    edit_meal = callback.data.split("_")[-1]
    edit_menu_date = (await state.get_data())['edit_menu_date']
    await state.update_data(edit_meal=edit_meal)

    meal_date = format_date(edit_menu_date)
    meal = menu_eng_to_ru[edit_meal].capitalize()
    menu = await get_meal_by_date(repo, edit_meal, edit_menu_date) or "Н/д"
    text = f'*Дата*: `{meal_date}`\n' \
           f'*Приём пищи*: `{meal}`\n' \
           f'*Меню*:\n' \
           f'```\n{menu}\n```\n\n' \
           'Чтобы изменить, отправьте *одним сообщением* изменённую версию.'

    await state.set_state(EditingMenu.writing)

    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(StateFilter(EditingMenu.writing), IsAdmin())
async def edit_cafe_menu_text_handler(
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


@router.callback_query(StateFilter(EditingMenu.writing), IsAdmin())
async def edit_cafe_menu_confirm_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
        repo: Repository,
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

    await repo.edit_meal_by_date(
        edit_meal, new_menu, edit_menu_date, callback.from_user.id
    )

    text = f'*{menu_eng_to_ru[edit_meal].capitalize()}* на ' \
           f'*{format_date(edit_menu_date)}* успешно изменён!'

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo, callback.from_user.id)
    )

    for new_menu_id in new_menu_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_menu_id
        )


@router.callback_query(F.data == CallbackData.UPLOAD_LESSONS, IsAdmin())
async def start_load_lessons_handler(
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


@router.message(
    StateFilter(LoadingLessons.image),
    F.content_type.in_({'photo'}),
    IsAdmin(),
)
async def load_lessons_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
) -> None:
    album = Album.model_validate(
        {
            "photo": [message.photo[-1]],
            "messages": [message],
            "caption": message.html_text,
        },
        context={"bot": message.bot}
    )
    await load_lessons_album_handler(message, state, repo, album)


@router.message(
    StateFilter(LoadingLessons.image),
    F.media_group_id,
    IsAdmin(),
)
async def load_lessons_album_handler(
        message: types.Message,
        state: FSMContext,
        repo: Repository,
        album: Album,
) -> None:
    """
    Обработчик сообщений с изображениями
    после нажатия кнопки "Загрузить уроки".
    """
    photos = album.photo
    proccess_results: list[str | tuple[str, date]] = []

    for photo in photos:
        photo_id = photo.file_id
        photo = await message.bot.get_file(photo_id)
        await message.bot.download_file(photo.file_path, image := BytesIO())

        result = await load_lessons_func(
            message.chat.id, image, message.bot, repo
        )
        proccess_results.append(result)

    if state:
        await state.clear()

    results: list[str] = []
    for result in proccess_results:
        if isinstance(result, tuple):
            grade, lessons_date = result
            results.append(
                f'Расписание для *{grade}-х классов* на '
                f'*{format_date(lessons_date)}* сохранено!'
            )
        else:
            results.append(result)

    text = '\n'.join(results)
    await message.reply(
        text=text,
        reply_markup=go_to_main_menu_keyboard
    )
