import datetime as dt

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import OpenMenu, StateData
from bot.utils.consts import TODAY
from bot.utils.enums import AdminCallback, TextCommands, UserCallback
from bot.utils.datehelp import date_today, format_date
from bot.utils.phrases import NO, YES


MAIN_MENU = "🏠Главное меню"
CANCEL = NOT_CONFIRM = f"{NO}Отмена"
CONFIRM = f"{YES}Подтвердить"


go_to_main_menu_button = InlineKeyboardButton(
    text=MAIN_MENU,
    callback_data=OpenMenu(menu=UserCallback.MAIN_MENU).pack(),
)

go_to_settings_button = InlineKeyboardButton(
    text=TextCommands.SETTINGS,
    callback_data=OpenMenu(menu=UserCallback.SETTINGS).pack(),
)

go_to_admin_panel_button = InlineKeyboardButton(
    text=TextCommands.ADMIN_PANEL,
    callback_data=AdminCallback.OPEN_ADMIN_PANEL,
)

cancel_state_button = InlineKeyboardButton(
    text=CANCEL,
    callback_data=StateData(action=UserCallback.CANCEL).pack(),
)

cancel_state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])

confirm_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=CONFIRM,
                callback_data=AdminCallback.CONFIRM,
            ),
            cancel_state_button,
        ],
    ],
)


def _left_right_keyboard_navigation(
    menu: str,
    today_smile: str,
    date: "dt.date" = None,
) -> "InlineKeyboardMarkup":
    """Клавиатура для меню с навигацией влево-вправо по датам.

    :param menu: Какое меню открывается.
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
            callback_data=OpenMenu(menu=menu, date=yesterday_data),
        )

    keyboard.button(
        text=f"{today_smile}Сегодня",
        callback_data=OpenMenu(menu=menu, date=TODAY),
    )

    if abs((today - tomorrow).days) < 7:
        keyboard.button(
            text=f"{tomorrow_str} ➡️",
            callback_data=OpenMenu(menu=menu, date=tomorrow_data),
        )

    keyboard.row(go_to_main_menu_button)

    return keyboard.as_markup()
