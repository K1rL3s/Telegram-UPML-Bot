from io import BytesIO
from uuid import uuid1

from aiocache import cached
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InputFile
from aiogram.utils.exceptions import Unauthorized
from loguru import logger

from src.database.db_funcs import update_user
from src.database.models.users import User


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


def tg_click_name(username: str, user_id: int) -> str:
    """
    Возвращает markdown строку с упоминанием пользователя.

    :param username: Отображаемое имя.
    :param user_id: ТГ Айди.
    """
    return f'[{username}](tg://user?id={user_id})'


def limit_min_max(
        value: int | float,
        minimum: int | float,
        maximum: int | float
) -> int | float:
    """
    Лимит числового значения по минмуму и максимум.
    """
    return max(
        min(value, maximum),
        minimum
    )


async def one_notify(
        text: str,
        user: User,
        keyboard: InlineKeyboardMarkup = None
) -> bool:
    """
    Делатель одного уведомления.

    :param text: Сообщение в уведомлении.
    :param user: Информация о пользователе.
    :param keyboard: Клавиатура на сообщении с уведомлением.
    """
    try:
        await Bot.get_current().send_message(
            text=text,
            chat_id=user.user_id,
            reply_markup=keyboard
        )
        logger.debug(f'Уведомление "{text}" успешно для {user.short_info()}')
        return True
    except Unauthorized:
        update_user(user.user_id, is_active=0)
        return True
    except Exception as e:
        logger.warning(f'Ошибка при уведомлении: {e}')
        return False
