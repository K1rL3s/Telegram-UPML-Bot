import base64
from io import BytesIO
from typing import TYPE_CHECKING, Union
from uuid import uuid1

from aiocache import cached
from aiogram.types import BufferedInputFile, User

if TYPE_CHECKING:
    from aiogram import Bot


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
    await message.delete()
    return message.photo[-1].file_id


async def multi_bytes_to_ids(
    chat_id: int,
    images: "Union[list[BytesIO], list[str]]",
    bot: "Bot",
) -> list[str]:
    """
    Перевод изображений из байтов в айдишники файлов телеграма.

    :param chat_id: Куда отправлять для сохранения.
    :param images: Файлы с расписаниями по классам.
    :param bot: ТГ Бот.
    :return: Айдишник полного расписания и айдишники отдельных расписаний.
    """
    return [
        await bytes_io_to_image_id(
            chat_id,
            image if isinstance(image, BytesIO) else BytesIO(base64.b64decode(image)),
            bot,
        )
        for image in images
    ]


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


def extract_username(from_user: "User") -> str | None:
    """
    Получение имени для бд из сообщения или нажатия кнопки.

    :param from_user: От кого событие.
    :return: Имя для бд.
    """
    return from_user.username or from_user.first_name or from_user.last_name  # XD


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
