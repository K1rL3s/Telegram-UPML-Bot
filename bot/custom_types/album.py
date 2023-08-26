"""Source: https://github.com/wakaree/simple_echo_bot."""

from aiogram.types import (
    Audio,
    Document,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
    PhotoSize,
    TelegramObject,
    Video,
)
from pydantic import Field


Media = PhotoSize | Video | Audio | Document
InputMedia = InputMediaPhoto | InputMediaVideo | InputMediaAudio | InputMediaDocument


INPUT_TYPES: dict[str, type[InputMedia]] = {
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
}


class Album(TelegramObject):
    """Telegram-Like объект для обработки сообщения с сгрупированными файлами."""

    photo: list["PhotoSize"] | None = None
    video: list["Video"] | None = None
    audio: list["Audio"] | None = None
    document: list["Document"] | None = None
    caption: str | None = None
    messages: list["Message"] = Field(default_factory=list)

    @property
    def media_types(self) -> list[str]:
        """Имеющиеся медиа-типы файлов в строковом виде."""
        return [media_type for media_type in INPUT_TYPES if getattr(self, media_type)]

    @property
    def as_media_group(self) -> list["InputMedia"]:
        """Преобразование имеющихся файлов в медиагруппу для отправки пользователю."""
        bot = self.bot
        group = [
            INPUT_TYPES[media_type](media=media.file_id, parse_mode=bot.parse_mode)
            for media_type in self.media_types
            for media in getattr(self, media_type)
        ]
        if group:
            group[0].caption = self.caption
        return group
