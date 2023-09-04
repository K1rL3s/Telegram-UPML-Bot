from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from bot.keyboards.universal import (
    go_to_admin_panel_button,
    go_to_main_menu_button,
    go_to_settings_button,
)
from bot.utils.enums import Roles, TextCommands, UserCallback


if TYPE_CHECKING:
    from bot.database.repository import UserRepository


go_to_main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[go_to_main_menu_button]],
)


async def main_menu_inline_keyboard(
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
            UserCallback.OPEN_CAFE_MENU_TODAY,
            UserCallback.OPEN_LESSONS_TODAY,
            UserCallback.OPEN_LAUNDRY,
            UserCallback.OPEN_ELECTIVES,
            UserCallback.OPEN_EDUCATORS_TODAY,
        ),
    ):
        keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=callback_data),
        )

    keyboard.add(go_to_settings_button)

    if await repo.is_has_any_role(user_id, [Roles.SUPERADMIN, Roles.ADMIN]):
        keyboard.add(go_to_admin_panel_button)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()


async def start_reply_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "ReplyKeyboardMarkup":
    """Клавиатура с текстовыми кнопками после команды /start."""
    inline_keyboard = await main_menu_inline_keyboard(repo, user_id)
    reply_keyboard = ReplyKeyboardBuilder()

    for row in inline_keyboard.inline_keyboard:
        for button in row:
            reply_keyboard.add(KeyboardButton(text=button.text))

    reply_keyboard.adjust(2, repeat=True)

    return reply_keyboard.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
