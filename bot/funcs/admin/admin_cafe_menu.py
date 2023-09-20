from typing import TYPE_CHECKING

from bot.funcs.admin.admin import get_meal_by_date
from bot.keyboards import cancel_state_keyboard, choose_meal_keyboard
from bot.utils.consts import CAFE_MENU_ENG_TO_RU
from bot.utils.datehelp import date_by_format, format_date, weekday_by_date
from bot.utils.phrases import NO
from bot.utils.states import EditingMenu

if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup
    from aiogram.fsm.context import FSMContext

    from bot.database.repository import MenuRepository


async def edit_cafe_menu_date_func(
    text: str,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup", int]:
    """
    Обработчик ввода даты для изменения меню.

    :param text: Сообщение пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатуру пользователю, айди сообщения бота.
    """
    if edit_date := date_by_format(text):
        text = (
            f"<b>Дата</b>: <code>{format_date(edit_date)}</code> "
            f"({weekday_by_date(edit_date)})\n"
            f"Какой приём пищи вы хотите изменить?"
        )
        keyboard = choose_meal_keyboard
        await state.set_state(EditingMenu.choose_meal)
        await state.update_data(edit_date=format_date(edit_date))
    else:
        text = f"{NO} Не удалось понять это как дату, попробуйте ещё раз."
        keyboard = cancel_state_keyboard

    return text, keyboard, (await state.get_data())["start_id"]


async def edit_cafe_menu_meal_func(
    callback_data: str,
    state: "FSMContext",
    repo: "MenuRepository",
) -> str:
    """
    Обработчик кнопки с выбором приёма пищи для изменения.

    :param callback_data: Callback строка.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний столовой.
    :return: Сообщение пользователю.
    """
    edit_meal = callback_data.split("_")[-1]
    edit_date = date_by_format((await state.get_data())["edit_date"])
    await state.update_data(edit_meal=edit_meal)

    meal = CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()
    menu = await get_meal_by_date(repo, edit_meal, edit_date)
    await state.set_state(EditingMenu.writing)

    return (
        f"<b>Дата</b>: <code>{format_date(edit_date)}</code> "
        f"({weekday_by_date(edit_date)})\n"
        f"<b>Приём пищи</b>: <code>{meal}</code>\n"
        f"<b>Меню:</b>\n"
        f"{menu}\n\n"
        "Чтобы изменить, отправьте <b>одним сообщением</b> изменённую версию."
    )


async def edit_cafe_menu_text_func(
    html_text: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с изменённой версией приёма пищи.

    :param html_text: Сообщение пользователя в html'е.
    :param message_id: Айди сообщения пользователя.
    :param state: Состояние пользователя.
    :return: Сообщение пользователю и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id = data["start_id"]
    edit_meal = data["edit_meal"]
    edit_date = date_by_format(data["edit_date"])

    new_ids = data.get("new_ids", []) + [message_id]
    await state.update_data(new_menu=html_text, new_ids=new_ids)
    meal = CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()
    text = (
        f"<b>Дата</b>: <code>{format_date(edit_date)}</code> "
        f"({weekday_by_date(edit_date)})\n"
        f"<b>Приём пищи</b>: <code>{meal}</code>\n"
        f"<b>Новое меню</b>:\n"
        f"{html_text}\n\n"
        "Для сохранения нажмите кнопку. "
        "Если хотите изменить, отправьте сообщение повторно."
    )

    return text, start_id


async def edit_cafe_menu_confirm_func(
    user_id: int,
    state: "FSMContext",
    repo: "MenuRepository",
) -> tuple[str, list[int]]:
    """
    Обработчик подтверждения изменения меню.

    :param user_id: ТГ Айди.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний столовой.
    :return: Сообщение пользователю и айдишники его сообщений с изменениями.
    """
    data = await state.get_data()
    edit_date = date_by_format(data["edit_date"])
    edit_meal = data["edit_meal"]
    new_menu = data["new_menu"]
    new_ids = data["new_ids"]

    await state.clear()

    await repo.update(edit_meal, new_menu, edit_date, user_id)

    text = (
        f"<b>{CAFE_MENU_ENG_TO_RU[edit_meal].capitalize()}</b> на "
        f"<b>{format_date(edit_date)} ({weekday_by_date(edit_date)})</b> "
        f"успешно изменён!"
    )

    return text, new_ids
