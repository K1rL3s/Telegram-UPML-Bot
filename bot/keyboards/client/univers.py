from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks import UniverData, UniversPaginator
from bot.keyboards.paginate import paginate_keyboard
from bot.keyboards.universal import (
    enrollee_menu_button,
    main_menu_button,
    univers_menu_button,
)
from shared.database.repository import UniverRepository
from shared.utils.enums import BotMenu, PageMenu


async def univers_cities_keyboard(
    page: int,
    univer_repo: UniverRepository,
) -> InlineKeyboardMarkup:
    subjects = [
        InlineKeyboardButton(
            text=city,
            callback_data=UniverData(city=city).pack(),
        )
        for city in await univer_repo.get_cities()
    ]

    return paginate_keyboard(
        buttons=subjects,
        page=page,
        menu=BotMenu.UNIVERS,
        rows=3,
        width=2,
        additional_buttons=[enrollee_menu_button],
    )


async def univers_titles_keyboard(
    page: int,
    city: str,
    univer_repo: UniverRepository,
) -> InlineKeyboardMarkup:
    univers = [
        InlineKeyboardButton(
            text=univer.title,
            callback_data=UniverData(city=city, id=univer.id, page=page).pack(),
        )
        for univer in await univer_repo.get_by_city(city)
    ]

    return paginate_keyboard(
        buttons=univers,
        page=page,
        menu=PageMenu.UNIVERS_LIST,
        rows=3,
        width=2,
        additional_buttons=[univers_menu_button],
        fabric=UniversPaginator,
        city=city,
    )


def one_univer_keyboard(city: str, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🏢 {city}",
                    callback_data=UniversPaginator(
                        menu=PageMenu.UNIVERS_LIST,
                        page=page,
                        city=city,
                    ).pack(),
                )
            ],
            [main_menu_button],
        ]
    )
