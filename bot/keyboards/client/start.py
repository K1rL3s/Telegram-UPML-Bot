from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)

from bot.keyboards.universal import (
    admin_panel_button,
    cafe_menu_button,
    educators_menu_button,
    electives_menu_button,
    enrollee_menu_button,
    laundry_menu_button,
    lessons_menu_button,
    main_menu_button,
    settings_button,
)
from shared.database.repository import UserRepository
from shared.utils.enums import RoleEnum

go_to_main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[main_menu_button]],
)


async def main_menu_keyboard(
    repo: "UserRepository",
    user_id: int,
) -> "InlineKeyboardMarkup":
    """Клавиатура главного меню."""
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        cafe_menu_button,
        lessons_menu_button,
        laundry_menu_button,
        electives_menu_button,
        educators_menu_button,
        enrollee_menu_button,
    )
    keyboard.adjust(2, repeat=True)

    keyboard.row(settings_button, width=1)

    if await repo.is_has_any_role(user_id, RoleEnum.all_roles()):
        keyboard.row(admin_panel_button, width=1)

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
