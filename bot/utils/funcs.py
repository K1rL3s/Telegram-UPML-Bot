from typing import TYPE_CHECKING, Union
from uuid import uuid1

from aiocache import cached
from aiogram.types import (
    BufferedInputFile,
    InlineKeyboardMarkup,
)
from aiogram.exceptions import TelegramUnauthorizedError
from loguru import logger

if TYPE_CHECKING:
    from io import BytesIO

    from aiogram import Bot
    from aiogram.types import CallbackQuery, Message

    from bot.database.models import User
    from bot.database.repository.repository import Repository


async def bytes_io_to_image_id(
    chat_id: int,
    image: "BytesIO",
    bot: "Bot",
) -> str:
    """
    Отправляет изображение, сохраняет его уникальный айди и удаляет это сообщение.

    :param chat_id: Куда отправлять.
    :param image: Что отправлять.
    :param bot: ТГ Бот.
    :return: Айди картинки.
    """
    image.seek(0)
    file = BufferedInputFile(image.read(), str(uuid1()))
    message = await bot.send_photo(
        chat_id=chat_id,
        photo=file,
    )
    file_id = message.photo[-1].file_id
    await message.delete()
    return file_id


@cached(ttl=60 * 60)
async def username_by_user_id(bot: "Bot", user_id: int) -> str | None:
    """
    Получение имени для бд по айди пользователя.

    :param bot: ТГ Бот.
    :param user_id: Айди юзера.
    :return: Имя для бд.
    """
    chat = await bot.get_chat(user_id)
    return chat.username or chat.first_name or chat.last_name


def extract_username(message: "Union[CallbackQuery, Message]") -> str | None:
    """
    Получение имени для бд из сообщения или нажатия кнопки.

    :param message: Событие.
    :return: Имя для бд.
    """
    return (
        message.from_user.username
        or message.from_user.first_name
        or message.from_user.last_name
    )  # XD


def name_link(username: str, user_id: int) -> str:
    """
    Возвращает markdown строку с упоминанием пользователя.

    :param username: Отображаемое имя.
    :param user_id: ТГ Айди.
    """
    return f"[{username}](tg://user?id={user_id})"


def limit_min_max(
    value: int | float,
    minimum: int | float,
    maximum: int | float,
) -> int | float:
    """Лимит числового значения по минмуму и максимум."""
    return max(min(value, maximum), minimum)


async def one_notify(
    bot: "Bot",
    repo: "Repository",
    user: "User",
    text: str,
    keyboard: "InlineKeyboardMarkup" = None,
) -> bool:
    """
    Делатель одного уведомления.

    :param bot: ТГ Бот.
    :param repo: Доступ к базе данных.
    :param user: Информация о пользователе.
    :param text: Сообщение в уведомлении.
    :param keyboard: Клавиатура на сообщении с уведомлением.
    """
    try:
        await bot.send_message(text=text, chat_id=user.user_id, reply_markup=keyboard)
        logger.debug(
            f'Уведомление "{" ".join(text.split())}" '
            f"успешно для {user.short_info()}",
        )
    except TelegramUnauthorizedError:
        await repo.user.update(user.user_id, is_active=0)
        return True
    except Exception as e:
        logger.warning(f"Ошибка при уведомлении: {e}")
        return False

    return True
