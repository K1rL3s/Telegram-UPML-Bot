from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from bot.callbacks import OpenMenu
from bot.keyboards.universal import (
    admin_panel_button,
    main_menu_button,
    settings_button,
)
from shared.utils.consts import TODAY
from shared.utils.enums import Menus, Roles, TextCommands

if TYPE_CHECKING:
    from shared.database.repository import UserRepository


go_to_main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[main_menu_button]],
)


async def main_menu_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "InlineKeyboardMarkup":
    """Клавиатура главного меню."""
    keyboard = InlineKeyboardBuilder()

    for button_text, callback_data in zip(
        (
            TextCommands.CAFE,
            TextCommands.LESSONS,
            TextCommands.LAUNDRY,
            TextCommands.ELECTIVES,
            TextCommands.EDUCATORS,
        ),
        (
            OpenMenu(menu=Menus.CAFE_MENU, date=TODAY),
            OpenMenu(menu=Menus.LESSONS, date=TODAY),
            OpenMenu(menu=Menus.LAUNDRY),
            OpenMenu(menu=Menus.ELECTIVES, date=TODAY),
            OpenMenu(menu=Menus.EDUCATORS, date=TODAY),
        ),
    ):
        keyboard.button(
            text=button_text,
            callback_data=callback_data.pack(),
        )

    keyboard.add(settings_button)

    if await repo.is_has_any_role(user_id, Roles.all_roles()):
        keyboard.add(admin_panel_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


async def start_reply_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "ReplyKeyboardMarkup":
    """Клавиатура с текстовыми кнопками после команды /start."""
    inline_keyboard = await main_menu_keyboard(repo, user_id)
    reply_keyboard = ReplyKeyboardBuilder()

    for row in inline_keyboard.inline_keyboard:
        for button in row:
            reply_keyboard.add(KeyboardButton(text=button.text))

    reply_keyboard.adjust(2, repeat=True)

    return reply_keyboard.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
