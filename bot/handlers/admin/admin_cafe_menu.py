from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.filters import IsAdmin
from bot.funcs.admin import get_meal_by_date
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
    choose_meal_keyboard,
    confirm_edit_keyboard,
)
from bot.upml.save_cafe_menu import process_cafe_menu
from bot.utils.consts import CAFE_MENU_ENG_TO_RU
from bot.utils.enums import AdminCallback
from bot.utils.datehelp import date_by_format, date_today, format_date
from bot.utils.states import EditingMenu

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.settings import Settings
    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == AdminCallback.AUTO_UPDATE_CAFE_MENU, IsAdmin())
async def auto_update_cafe_menu_handler(
    callback: "CallbackQuery",
    settings: "Settings",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Загрузить меню".

    Загружает и обрабатывает PDF расписание еды с сайта лицея.
    """
    _, text = await process_cafe_menu(repo.menu, settings.other.TIMEOUT)

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )


@router.callback_query(F.data == AdminCallback.EDIT_CAFE_MENU, IsAdmin())
async def edit_cafe_menu_start_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обрабочтки кнопки "Изменить меню"."""
    text = f"""
Введите дату дня, меню которого хотите изменить в формате *ДД.ММ.ГГГГ*
Например, `{format_date(date_today())}`
""".strip()

    await state.set_state(EditingMenu.choose_date)
    await state.set_data({"start_id": callback.message.message_id})

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingMenu.choose_date), IsAdmin())
async def edit_cafe_menu_date_handler(message: "Message", state: "FSMContext") -> None:
    """Обработчик ввода доты для изменения меню."""
    if not (edit_date := date_by_format(message.text)):  # is False
        text = f'Не удалось понять дату "`{message.text}`", попробуйте ещё раз'
        keyboard = cancel_state_keyboard
    else:
        text = (
            f"*Дата*: `{format_date(edit_date)}`\n"
            f"Какой приём пищи вы хотите изменить?"
        )
        keyboard = choose_meal_keyboard
        await state.set_state(EditingMenu.choose_meal)
        await state.update_data(edit_date=edit_date)

    start_id = (await state.get_data())["start_id"]

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=keyboard,
    )

    await message.delete()  # ?


@router.callback_query(StateFilter(EditingMenu.choose_meal), IsAdmin())
async def edit_cafe_menu_meal_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки с выбором приёма пищи для изменения."""
    edit_meal = callback.data.split("_")[-1]
    edit_date = (await state.get_data())["edit_date"]
    await state.update_data(edit_meal=edit_meal)

    meal_date = format_date(edit_date)
    meal = CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()
    menu = await get_meal_by_date(repo.menu, edit_meal, edit_date)
    text = (
        f"*Дата*: `{meal_date}`\n"
        f"*Приём пищи*: `{meal}`\n"
        f"*Меню*:\n"
        f"```\n{menu}\n```\n\n"
        "Чтобы изменить, отправьте *одним сообщением* изменённую версию."
    )

    await state.set_state(EditingMenu.writing)

    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingMenu.writing), IsAdmin())
async def edit_cafe_menu_text_handler(
    message: "Message",
    state: "FSMContext",
) -> None:
    """Обработчик сообщения с изменённой версией приёма пищи."""
    data = await state.get_data()
    start_id = data["start_id"]
    edit_date = data["edit_date"]
    edit_meal = data["edit_meal"]

    new_menu = message.text
    new_menu_ids = data.get("new_menu_ids", [])
    new_menu_ids.append(message.message_id)
    await state.update_data(new_menu=new_menu, new_menu_ids=new_menu_ids)

    text = (
        f"*Дата*: `{format_date(edit_date)}`\n"
        f"*Приём пищи*: `{CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()}`\n"
        f"*Новое меню*:\n```\n{new_menu}```\n\n"
        "Для сохранения нажмите кнопку. Если хотите изменить, "
        "отправьте сообщение повторно."
    )

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=start_id,
        reply_markup=confirm_edit_keyboard,
    )


@router.callback_query(StateFilter(EditingMenu.writing), IsAdmin())
async def edit_cafe_menu_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик подтверждения изменения меню."""
    data = await state.get_data()
    edit_date = data["edit_date"]
    edit_meal = data["edit_meal"]
    new_menu = data["new_menu"]
    new_menu_ids = data["new_menu_ids"]

    await state.clear()

    await repo.menu.update(edit_meal, new_menu, edit_date, callback.from_user.id)

    text = (
        f"*{CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()}* на "
        f"*{format_date(edit_date)}* успешно изменён!"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )

    for new_menu_id in new_menu_ids:
        await callback.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=new_menu_id,
        )
