from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks import OlympData, OlympsPaginator
from bot.keyboards.paginate import paginate_keyboard
from bot.keyboards.universal import (
    DELETE,
    enrollee_menu_button,
    main_menu_button,
    olymps_menu_button,
)
from shared.database.repository import OlympRepository
from shared.utils.enums import Action, BotMenu, PageMenu


async def olymps_subjects_keyboard(
    page: int,
    olymp_repo: OlympRepository,
) -> InlineKeyboardMarkup:
    subjects = [
        InlineKeyboardButton(
            text=subject,
            callback_data=OlympData(subject=subject, page=page).pack(),
        )
        for subject in await olymp_repo.get_subjects()
    ]

    return paginate_keyboard(
        buttons=subjects,
        page=page,
        menu=BotMenu.OLYMPS,
        rows=3,
        width=2,
        additional_buttons=[enrollee_menu_button],
    )


async def olymps_titles_keyboard(
    page: int,
    subject: str,
    olymp_repo: OlympRepository,
) -> InlineKeyboardMarkup:
    olymps = [
        InlineKeyboardButton(
            text=olymp.title,
            callback_data=OlympData(subject=subject, id=olymp.id, page=page).pack(),
        )
        for olymp in await olymp_repo.get_by_subject(subject)
    ]

    return paginate_keyboard(
        buttons=olymps,
        page=page,
        menu=PageMenu.OLYMPS_LIST,
        rows=3,
        width=2,
        additional_buttons=[olymps_menu_button],
        fabric=OlympsPaginator,
        subject=subject,
    )


def one_olymp_keyboard(
    olymp_id: int,
    subject: str,
    page: int,
    add_edit_buttons: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=f"🏆 {subject}",
            callback_data=OlympsPaginator(
                menu=PageMenu.OLYMPS_LIST, page=page, subject=subject
            ).pack(),
        ),
        width=1,
    )

    if add_edit_buttons:
        builder.row(
            InlineKeyboardButton(
                text=DELETE,
                callback_data=OlympData(
                    action=Action.DELETE,
                    subject=subject,
                    id=olymp_id,
                    page=page,
                ).pack(),
            ),
            width=1,
        )

    builder.row(main_menu_button, width=1)

    return builder.as_markup()
