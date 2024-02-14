import datetime as dt

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from bot.keyboards import cancel_state_keyboard, choose_meal_keyboard
from shared.database.repository import MenuRepository
from shared.utils.datehelp import (
    date_by_format,
    date_today,
    format_date,
    weekday_by_date,
)
from shared.utils.phrases import NO, NO_DATA
from shared.utils.states import EditingMenu
from shared.utils.translate import CAFE_MENU_TRANSLATE


async def edit_cafe_menu_start_func(
    message_id: int,
    state: "FSMContext",
) -> str:
    """
    Обрабочтки кнопки "Изменить меню".

    :param message_id: Начальное сообщение бота.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура для пользователя.
    """
    await state.set_state(EditingMenu.choose_date)
    await state.update_data(start_id=message_id)

    return f"""
Введите дату дня, меню которого хотите изменить в формате <b>ДД.ММ.ГГГГ</b>
Например, <code>{format_date(date_today())}</code>
""".strip()


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
    edit_meal: str,
    state: "FSMContext",
    repo: "MenuRepository",
) -> str:
    """
    Обработчик кнопки с выбором приёма пищи для изменения.

    :param edit_meal: Какой приём пищи изменяется.
    :param state: Состояние пользователя.
    :param repo: Репозиторий расписаний столовой.
    :return: Сообщение пользователю.
    """
    await state.set_state(EditingMenu.write)
    data = await state.update_data(edit_meal=edit_meal)

    edit_date: "dt.date" = date_by_format(data["edit_date"])
    menu = getattr(await repo.get(edit_date), edit_meal, None) or NO_DATA
    meal = CAFE_MENU_TRANSLATE[edit_meal].capitalize()

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
    start_id: int = data["start_id"]
    edit_meal: str = data["edit_meal"]
    edit_date: "dt.date" = date_by_format(data["edit_date"])

    new_ids: list[int] = data.get("new_ids", []) + [message_id]
    await state.update_data(new_menu=html_text, new_ids=new_ids)
    meal = CAFE_MENU_TRANSLATE[edit_meal].capitalize()
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
    edit_date: "dt.date" = date_by_format(data["edit_date"])
    edit_meal: str = data["edit_meal"]
    new_menu: str = data["new_menu"]
    new_ids: list[int] = data["new_ids"]

    await state.clear()

    await repo.update(edit_meal, new_menu, edit_date, user_id)

    text = (
        f"<b>{CAFE_MENU_TRANSLATE[edit_meal].capitalize()}</b> на "
        f"<b>{format_date(edit_date)} ({weekday_by_date(edit_date)})</b> "
        f"успешно изменён!"
    )

    return text, new_ids
