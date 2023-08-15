"""
Source:
https://github.com/wakaree/simple_echo_bot
"""

from typing import Type, Union, cast

from aiogram import Bot
from aiogram.types import (
    Audio, Document, PhotoSize, Video,
    InputMediaPhoto, InputMediaVideo,
    InputMediaAudio, InputMediaDocument,
    Message, TelegramObject,
)
from pydantic import Field


Media = Union[PhotoSize, Video, Audio, Document]
InputMedia = Union[
    InputMediaPhoto, InputMediaVideo,
    InputMediaAudio, InputMediaDocument,
]

INPUT_TYPES: dict[str, Type[InputMedia]] = {
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
}


class Album(TelegramObject):
    photo: list[PhotoSize] | None = None
    video: list[Video] | None = None
    audio: list[Audio] | None = None
    document: list[Document] | None = None
    caption: str | None = None
    messages: list[Message] = Field(default_factory=list)

    @property
    def media_types(self) -> list[str]:
        return [
            media_type
            for media_type in INPUT_TYPES
            if getattr(self, media_type)
        ]

    @property
    def as_media_group(self) -> list[InputMedia]:
        bot = cast(Bot, self.bot)
        group = [
            INPUT_TYPES[media_type](
                media=media.file_id,
                parse_mode=bot.parse_mode
            )
            for media_type in self.media_types
            for media in getattr(self, media_type)
        ]
        if group:
            group[0].caption = self.caption
        return group