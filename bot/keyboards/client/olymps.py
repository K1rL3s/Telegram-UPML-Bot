from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks import OlympsData
from bot.keyboards.paginate import paginate_keyboard
from bot.keyboards.universal import enrollee_menu_button
from shared.database.repository import OlympRepository
from shared.utils.enums import BotMenu


async def olymps_subjects_keyboard(
    page: int, olymp_repo: OlympRepository
) -> InlineKeyboardMarkup:
    menu = BotMenu.OLYMPS

    subjects = [
        InlineKeyboardButton(
            text=subject.capitalize(),
            callback_data=OlympsData(subject=subject).pack(),
        )
        for subject in await olymp_repo.get_subjects()
    ]

    return paginate_keyboard(
        buttons=subjects,
        page=page,
        menu=menu,
        rows=3,
        width=2,
        additional_buttons=[enrollee_menu_button],
    )
