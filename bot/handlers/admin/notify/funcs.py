from typing import TYPE_CHECKING, Any, Union

from sqlalchemy.orm import Mapped, MappedColumn

from bot.keyboards import (
    cancel_state_keyboard,
    notify_for_class_keyboard,
    notify_for_grade_keyboard,
)
from shared.database.models import Settings, User
from shared.utils.enums import NotifyType
from shared.utils.notify import do_admin_notify
from shared.utils.states import DoingNotify
from shared.utils.translate import NOTIFIES_TYPES_TRANSLATE

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.types import InlineKeyboardMarkup

    from shared.database.repository import UserRepository


async def notify_for_who_func(
    notify_type: str,
    for_who: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, "InlineKeyboardMarkup"]:
    """
    Обработчик нажатия одной из кнопок уведомления в панели уведомлений.

    :param notify_type: Тип уведомления.
    :param for_who: Для кого уведомление.
    :param message_id: Айди начального сообщения бота.
    :param state: Состояние пользователя.
    :return: Сообщение и клавиатура для пользователя.
    """
    if notify_type == NotifyType.GRADE:
        text = "Выберите, каким классам сделать уведомление"
        keyboard = notify_for_grade_keyboard
    elif notify_type == NotifyType.CLASS:
        text = "Выберите, какому классу сделать уведомление"
        keyboard = notify_for_class_keyboard
    else:
        await state.set_state(DoingNotify.writing)
        await state.set_data(
            {
                "start_id": message_id,
                # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
                "for_who": for_who,
            },
        )
        text = (
            f"Тип: <code>{NOTIFIES_TYPES_TRANSLATE.get(for_who, for_who)}</code>\n"
            "Напишите сообщение, которое будет в уведомлении"
        )
        keyboard = cancel_state_keyboard

    return text, keyboard


async def notify_message_func(
    html_text: str,
    message_id: int,
    state: "FSMContext",
) -> tuple[str, int]:
    """
    Обработчик сообщения с текстом для рассылки.

    :param html_text: Сообщение пользователя в html'е.
    :param message_id: Айди сообщения юзера.
    :param state: Состояние пользователя.
    :return: Сообщение и айди начального сообщения бота.
    """
    data = await state.get_data()
    start_id: int = data["start_id"]
    for_who: str = data["for_who"]

    messages_ids = data.get("messages_ids", [])
    messages_ids.append(message_id)
    await state.update_data(html_text=html_text, messages_ids=messages_ids)

    text = (
        f"Тип: <code>{NOTIFIES_TYPES_TRANSLATE.get(for_who, for_who)}</code>\n"
        f"Сообщение:\n{html_text}\n\n"
        "Для отправки нажмите кнопку. Если хотите изменить, "
        "отправьте сообщение повторно."
    )

    return text, start_id


async def notify_confirm_func(
    user_id: int,
    bot: "Bot",
    state: "FSMContext",
    repo: "UserRepository",
) -> tuple[str, list[int]]:
    """
    Обработчик подтверждения отправки рассылки.

    :param user_id: ТГ Айди.
    :param bot: ТГ Бот.
    :param state: Состояние пользователя.
    :param repo: Репозиторий пользователей.
    :return: Сообщение пользователю и айдишники его сообщений с изменениями.
    """
    data = await state.get_data()
    for_who: str = data["for_who"]
    html_text: str = data["html_text"]
    messages_ids: list[int] = data["messages_ids"]
    await state.clear()

    users = await get_users_for_notify(repo, for_who, is_news=True)
    await do_admin_notify(
        html_text,
        users,
        user_id,
        NOTIFIES_TYPES_TRANSLATE.get(for_who, for_who),
        bot,
        repo,
    )

    return "Рассылка завершена!", messages_ids


async def get_users_for_notify(
    repo: "UserRepository",
    for_who: str,  # all, grade_10, grade_11, 10А, 10Б, 10В, 11А, 11Б, 11В
    is_lessons: bool = False,
    is_news: bool = False,
) -> list["User"]:
    """Пользователи для рассылки по условиями.

    Преобразует notify_type из `async def notify_for_who_handler` в условия для фильтра.

    :param repo: Репозиторий пользователей.
    :param for_who: Кому уведомление.
    :param is_lessons: Уведомление об изменении расписания.
    :param is_news: Уведомление о новостях (ручная рассылка).
    """
    conditions: "list[tuple[Union[MappedColumn, Mapped], Any]]" = [
        (User.is_active, True)
    ]

    if is_lessons:
        conditions.append((Settings.lessons_notify, True))
    if is_news:
        conditions.append((Settings.news_notify, True))

    if for_who.startswith("grade"):
        conditions.append((Settings.grade, for_who.split("_")[-1]))
    elif (
        len(for_who) == 3
        and any(for_who.startswith(grade) for grade in ("10", "11"))
        and any(for_who.endswith(letter) for letter in "АБВ")
    ):  # XD
        conditions.append((Settings.class_, for_who))

    return await repo.get_by_conditions(conditions)
