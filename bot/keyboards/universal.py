import datetime as dt

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import InStateData, OpenMenu
from shared.utils.consts import TODAY
from shared.utils.datehelp import date_today, format_date
from shared.utils.enums import Actions, Menus, TextCommands
from shared.utils.phrases import NO, YES

MAIN_MENU = "🏠Главное меню"
CANCEL = f"{NO}Отмена"
CONFIRM = f"{YES}Подтвердить"


main_menu_button = InlineKeyboardButton(
    text=MAIN_MENU,
    callback_data=OpenMenu(menu=Menus.MAIN_MENU).pack(),
)
settings_button = InlineKeyboardButton(
    text=TextCommands.SETTINGS,
    callback_data=OpenMenu(menu=Menus.SETTINGS).pack(),
)
admin_panel_button = InlineKeyboardButton(
    text=TextCommands.ADMIN_PANEL,
    callback_data=OpenMenu(menu=Menus.ADMIN_PANEL).pack(),
)
confirm_state_button = InlineKeyboardButton(
    text=CONFIRM,
    callback_data=InStateData(action=Actions.CONFIRM).pack(),
)
cancel_state_button = InlineKeyboardButton(
    text=CANCEL,
    callback_data=InStateData(action=Actions.CANCEL).pack(),
)

cancel_state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])

confirm_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_state_button, cancel_state_button]],
)


def _left_right_keyboard_navigation(
    bot_menu: str,
    today_smile: str,
    date: "dt.date" = None,
) -> "InlineKeyboardMarkup":
    """Клавиатура для меню с навигацией влево-вправо по датам.

    :param bot_menu: Какое меню открывается.
    :param today_smile: Смайлик на кнопке "Сегодня".
    :param date: Дата, на которой открыта навигация. None - сегодня.
    :return: Клавиатура меню навигации влево-вправо.
    """
    today = date_today()

    if date is None:
        date = today

    tomorrow = date + dt.timedelta(days=1)
    yesterday = date - dt.timedelta(days=1)
    tomorrow_str = format_date(tomorrow, with_year=False)
    yesterday_str = format_date(yesterday, with_year=False)
    tomorrow_data = format_date(tomorrow)
    yesterday_data = format_date(yesterday)

    keyboard = InlineKeyboardBuilder()

    if abs((today - yesterday).days) < 7:
        keyboard.button(
            text=f"⬅️ {yesterday_str}",
            callback_data=OpenMenu(menu=bot_menu, date=yesterday_data),
        )

    keyboard.button(
        text=f"{today_smile}Сегодня",
        callback_data=OpenMenu(menu=bot_menu, date=TODAY),
    )

    if abs((today - tomorrow).days) < 7:
        keyboard.button(
            text=f"{tomorrow_str} ➡️",
            callback_data=OpenMenu(menu=bot_menu, date=tomorrow_data),
        )

    keyboard.row(main_menu_button)

    return keyboard.as_markup()
