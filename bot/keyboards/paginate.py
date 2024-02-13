from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ButtonType, InlineKeyboardBuilder

from bot.callbacks import Paginator
from bot.keyboards.universal import main_menu_button

PAGE_BACK = "⬅️Назад"
PAGE_FORWARD = "➡️Вперёд"


def paginate_keyboard(
    buttons: list[ButtonType],
    page: int,
    menu: str,
    rows: int = 3,
    width: int = 2,
    additional_buttons: list[InlineKeyboardButton] = None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    bpp = rows * width  # Кнопок на страницу (buttons per page)

    start, end = page * bpp, page * bpp + bpp

    builder.add(*buttons[start:end])
    builder.adjust(width)

    left_right: list[ButtonType] = []
    if page > 0:
        left_right.append(
            InlineKeyboardButton(
                text=PAGE_BACK,
                callback_data=Paginator(menu=menu, page=page - 1).pack(),
            )
        )
    if end < len(buttons):
        left_right.append(
            InlineKeyboardButton(
                text=PAGE_FORWARD,
                callback_data=Paginator(menu=menu, page=page + 1).pack(),
            )
        )
    builder.row(*left_right, width=2)

    if additional_buttons:
        builder.row(*additional_buttons, width=len(additional_buttons))

    builder.row(main_menu_button, width=1)

    return builder.as_markup()


if __name__ == "__main__":
    btns = [
        InlineKeyboardButton(text=f"{i}", callback_data="123") for i in range(1, 60 + 1)
    ]
    keyboard = paginate_keyboard(
        buttons=btns,
        page=0,
        menu="smtmenu",
        rows=10,
        width=3,
        additional_buttons=[
            InlineKeyboardButton(text="BACKBUTTON", callback_data="3456")
        ],
    )
    for row in keyboard.inline_keyboard:
        print(row)
