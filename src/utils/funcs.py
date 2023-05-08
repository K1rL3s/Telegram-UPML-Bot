from io import BytesIO
from uuid import uuid1

from aiogram import Bot
from aiogram.types import InputFile


async def bytes_io_to_image_id(
        chat_id: int,
        image: BytesIO,
) -> str:
    image.seek(0)
    file = InputFile(image, filename=str(uuid1()))
    message = await Bot.get_current().send_photo(
        chat_id=chat_id,
        photo=file,
    )
    file_id = message.photo[-1].file_id
    # await message.delete()
    return file_id
