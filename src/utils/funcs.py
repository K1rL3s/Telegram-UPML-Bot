from io import BytesIO
from uuid import uuid1

from aiocache import cached
from aiogram import Bot, types
from aiogram.types import InputFile


async def bytes_io_to_image_id(
        chat_id: int,
        image: BytesIO,
) -> str:
    """
    Отправляет изображение в телеграм, сохраняет его уникальный айди
    и удаляет это сообщение.

    :param chat_id: Куда отправлять.
    :param image: Что отправлять.
    :return: Айди картинки.
    """

    image.seek(0)
    file = InputFile(image, filename=str(uuid1()))
    message = await Bot.get_current().send_photo(
        chat_id=chat_id,
        photo=file,
    )
    file_id = message.photo[-1].file_id
    await message.delete()
    return file_id


@cached(ttl=60 * 60)
async def username_by_user_id(user_id: int) -> str | None:
    """
    Получение имени для бд по айди пользователя.

    :param user_id: Айди юзера.
    :return: Имя для бд.
    """
    chat = await Bot.get_current().get_chat(user_id)
    return chat.username or chat.first_name or chat.last_name


def extract_username(
        message: types.CallbackQuery | types.Message
) -> str | None:
    """
    Получение имени для бд из сообщения или нажатия кнопки.

    :param message: Событие.
    :return: Имя для бд.
    """

    return (
            message.from_user.username or
            message.from_user.first_name or
            message.from_user.last_name
    )  # XD
