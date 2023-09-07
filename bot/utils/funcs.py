from typing import TYPE_CHECKING, Union
from uuid import uuid1

from aiocache import cached
from aiogram.types import BufferedInputFile

if TYPE_CHECKING:
    from io import BytesIO

    from aiogram import Bot
    from aiogram.types import CallbackQuery, Message


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
    return f'<a href="tg://user?id={user_id}">{username}</a>'


def laundry_limit_min_max(
    value: int | float,
    minimum: int | float = 1,
    maximum: int | float = 2 * 24 * 60,  # Двое суток
) -> int | float:
    """
    Лимит времени таймера прачечной.

    :param value: Введёное число.
    :param minimum: Минимальное значение.
    :param maximum: Максимальное значение.
    """
    return max(min(value, maximum), minimum)
