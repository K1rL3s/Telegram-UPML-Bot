import asyncio
from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramForbiddenError
from loguru import logger

from shared.utils.consts import NOTIFIES_PER_BATCH
from shared.utils.funcs import name_link, username_by_user_id

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup

    from shared.database.models import User
    from shared.database.repository import UserRepository


async def do_one_notify(
    text: str,
    bot: "Bot",
    repo: "UserRepository",
    user: "User",
    keyboard: "InlineKeyboardMarkup" = None,
) -> bool:
    """
    Делатель одного уведомления.

    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    :param user: Информация о пользователе.
    :param text: Сообщение в уведомлении.
    :param keyboard: Клавиатура на сообщении с уведомлением.
    """
    try:
        await bot.send_message(text=text, chat_id=user.user_id, reply_markup=keyboard)
        logger.debug(
            "Уведомление успешно [{short_info}]",
            short_info=user.short_info,
        )
    except TelegramForbiddenError:
        await repo.update(user.user_id, is_active=False)
        return False
    except Exception as e:
        logger.warning(
            "Ошибка при уведомлении: {err} [{short_info}]",
            err=e,
            short_info=user.short_info,
        )
        return False

    return True


async def do_many_notifies(
    text: str,
    users: list["User"],
    bot: "Bot",
    repo: "UserRepository",
) -> None:
    """
    Рассылка текста пользователям в одновременном режиме.

    :param text: Текст рассылки.
    :param users: Пользователи, которым должна прийти рассылка.
    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    """
    for i in range(0, len(users), NOTIFIES_PER_BATCH):
        tasks = [
            asyncio.create_task(do_one_notify(text, bot, repo, user))
            for user in users[i : i + NOTIFIES_PER_BATCH]
        ]
        timer = asyncio.create_task(asyncio.sleep(1))
        await asyncio.gather(*tasks)
        await timer


async def do_admin_notify(
    text: str,
    users: list["User"],
    from_who: int,
    for_who: str,
    bot: "Bot",
    repo: "UserRepository",
) -> None:
    """
    Делатель рассылки от администратора.

    :param text: Сообщение администратора.
    :param users: Кому отправить сообщение.
    :param from_who: ТГ Айди отправителя (админа)
    :param for_who: Для кого рассылка.
    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    """
    username = await username_by_user_id(bot, from_who)
    text = (
        "🔔<b>Уведомление от администратора</b> "
        f"{name_link(username, from_who)} <b>{for_who}</b>\n\n" + text
    )
    await do_many_notifies(text, users, bot, repo)
