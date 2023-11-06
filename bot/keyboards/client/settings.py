from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.callbacks import OpenMenu, SettingsData
from bot.keyboards.universal import main_menu_button
from bot.utils.consts import GRADES
from bot.utils.datehelp import format_time
from bot.utils.enums import Actions, Menus, UserCallback
from bot.utils.phrases import NO, QUESTION, YES

if TYPE_CHECKING:
    from bot.database.repository import SettingsRepository


USER_CLASS = "Класс {0}".format
LESSONS_NOTIFY = "Уроки {0}".format
NEWS_NOTIFY = "Новости {0}".format

WASHING = "⏳Стирка: {0}".format
DRYING = "💨Сушка: {0}".format
BACK_TO_SETTINGS = "⏪Настройки"
RESET_CLASS = f"{QUESTION}Сбросить класс"


async def settings_keyboard(
    repo: "SettingsRepository",
    user_id: int,
) -> "InlineKeyboardMarkup":
    """Клавиатура настроек, своя у каждого пользователя."""
    settings = await repo.get(user_id)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=USER_CLASS(settings.class_ if settings.class_ else QUESTION),
                    callback_data=SettingsData(action=UserCallback.CHANGE_GRADE).pack(),
                ),
                InlineKeyboardButton(
                    text=LESSONS_NOTIFY(YES if settings.lessons_notify else NO),
                    callback_data=SettingsData(
                        action=Actions.SWITCH,
                        attr=UserCallback.LESSONS_NOTIFY,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=NEWS_NOTIFY(YES if settings.news_notify else NO),
                    callback_data=SettingsData(
                        action=Actions.SWITCH,
                        attr=UserCallback.NEWS_NOTIFY,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text=WASHING(
                        f"{settings.washing_minutes} мин."
                        if settings.washing_time is None
                        else format_time(settings.washing_time),
                    ),
                    callback_data=SettingsData(
                        action=Actions.EDIT,
                        attr=UserCallback.WASHING,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=DRYING(
                        f"{settings.drying_minutes} мин."
                        if settings.drying_time is None
                        else format_time(settings.drying_time),
                    ),
                    callback_data=SettingsData(
                        action=Actions.EDIT,
                        attr=UserCallback.DRYING,
                    ).pack(),
                ),
            ],
            [main_menu_button],
        ],
    )


choose_grade_keyboard: "InlineKeyboardMarkup" = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=grade_letter,
                callback_data=SettingsData(
                    action=UserCallback.CHANGE_GRADE,
                    attr=grade_letter,
                ).pack(),
            )
            for grade_letter in GRADES
        ),
        InlineKeyboardButton(
            text=BACK_TO_SETTINGS,
            callback_data=OpenMenu(menu=Menus.SETTINGS).pack(),
        ),
        InlineKeyboardButton(
            text=RESET_CLASS,
            callback_data=SettingsData(
                action=UserCallback.CHANGE_GRADE,
                attr=UserCallback.EMPTY,
            ).pack(),
        ),
    )
    .adjust(3, 3, 2)
    .as_markup()
)
