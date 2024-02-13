import datetime as dt

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import InStateData, OpenMenu
from shared.utils.consts import TODAY
from shared.utils.datehelp import date_today, format_date
from shared.utils.enums import Action, BotMenu, TextCommand
from shared.utils.phrases import NO, YES

MAIN_MENU = "🏠Главное меню"
CANCEL = f"{NO}Отмена"
CONFIRM = f"{YES}Подтвердить"


main_menu_button = InlineKeyboardButton(
    text=MAIN_MENU,
    callback_data=OpenMenu(menu=BotMenu.MAIN_MENU).pack(),
)
settings_button = InlineKeyboardButton(
    text=TextCommand.SETTINGS,
    callback_data=OpenMenu(menu=BotMenu.SETTINGS).pack(),
)
admin_panel_button = InlineKeyboardButton(
    text=TextCommand.ADMIN_PANEL,
    callback_data=OpenMenu(menu=BotMenu.ADMIN_PANEL).pack(),
)
cafe_menu_button = InlineKeyboardButton(
    text=TextCommand.CAFE,
    callback_data=OpenMenu(menu=BotMenu.CAFE_MENU, date=TODAY).pack(),
)
lessons_menu_button = InlineKeyboardButton(
    text=TextCommand.LESSONS,
    callback_data=OpenMenu(menu=BotMenu.LESSONS, date=TODAY).pack(),
)
laundry_menu_button = InlineKeyboardButton(
    text=TextCommand.LAUNDRY,
    callback_data=OpenMenu(menu=BotMenu.LAUNDRY).pack(),
)
electives_menu_button = InlineKeyboardButton(
    text=TextCommand.ELECTIVES,
    callback_data=OpenMenu(menu=BotMenu.ELECTIVES, date=TODAY).pack(),
)
educators_menu_button = InlineKeyboardButton(
    text=TextCommand.EDUCATORS,
    callback_data=OpenMenu(menu=BotMenu.EDUCATORS, date=TODAY).pack(),
)
enrollee_menu_button = InlineKeyboardButton(
    text=TextCommand.ENROLLEE,
    callback_data=OpenMenu(menu=BotMenu.ENROLLEE).pack(),
)
univers_menu_button = InlineKeyboardButton(
    text=TextCommand.UNIVERS,
    callback_data=OpenMenu(menu=BotMenu.UNVIVERS).pack(),
)
olymps_menu_button = InlineKeyboardButton(
    text=TextCommand.OLYMPS,
    callback_data=OpenMenu(menu=BotMenu.OLYMPS).pack(),
)
confirm_state_button = InlineKeyboardButton(
    text=CONFIRM,
    callback_data=InStateData(action=Action.CONFIRM).pack(),
)
cancel_state_button = InlineKeyboardButton(
    text=CANCEL,
    callback_data=InStateData(action=Action.CANCEL).pack(),
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
