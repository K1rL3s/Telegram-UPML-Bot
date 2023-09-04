import asyncio
from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from loguru import logger

from bot.utils.consts import NOTIFIES_PER_BATCH
from bot.utils.funcs import name_link, username_by_user_id

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import InlineKeyboardMarkup

    from bot.database.models import User
    from bot.database.repository import UserRepository


async def one_notify(
    bot: "Bot",
    repo: "UserRepository",
    user: "User",
    text: str,
    keyboard: "InlineKeyboardMarkup" = None,
    try_count: int = 1,
) -> bool:
    """
    Делатель одного уведомления.

    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    :param user: Информация о пользователе.
    :param text: Сообщение в уведомлении.
    :param keyboard: Клавиатура на сообщении с уведомлением.
    :param try_count: Попытка отправки (для повтора при превышении rps).
    """
    try:
        await bot.send_message(text=text, chat_id=user.user_id, reply_markup=keyboard)
        logger.debug(
            f'Уведомление "{" ".join(text.split())}" '
            f"успешно для {user.short_info()}",
        )
    except TelegramForbiddenError:
        await repo.update(user.user_id, is_active=0)
        return True
    except TelegramRetryAfter:
        await asyncio.sleep(try_count**2)
        return await one_notify(bot, repo, user, text, keyboard, try_count + 1)
    except Exception as e:
        logger.warning(f"Ошибка при уведомлении: {e} [{user.short_info()}]")
        return False

    return True


async def do_admin_notifies(
    bot: "Bot",
    repo: "UserRepository",
    text: str,
    users: list["User"],
    from_who: int = 0,
    for_who: str = "",
) -> None:
    """
    Делатель рассылки от администратора.

    :param bot: ТГ Бот.
    :param repo: Репозиторий пользователей.
    :param text: Сообщение.
    :param users: Кому отправить сообщение.
    :param from_who: ТГ Айди отправителя (админа)
    :param for_who: Для кого рассылка.
    """
    username = await username_by_user_id(bot, from_who)
    text = (
        "🔔*Уведомление от администратора* "
        f"{name_link(username, from_who)} *{for_who}*\n\n" + text
    )

    for i in range(0, len(users), NOTIFIES_PER_BATCH):
        tasks = [
            asyncio.create_task(one_notify(bot, repo, user, text))
            for user in users[i : i + NOTIFIES_PER_BATCH]
        ]
        # Из-за рекурсивного вызова one_notify при TelegramRetryAfter
        # может задерживать всю рассылку.
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)
