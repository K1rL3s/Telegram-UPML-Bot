"""
Source:
https://github.com/wakaree/simple_echo_bot
"""

from asyncio import sleep
from typing import Any, Callable, Awaitable, Final, MutableMapping, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from bot.custom_types import Album, Media


ALBUM_KEY: Final[str] = "album"


class AlbumMiddleware(BaseMiddleware):
    DEFAULT_LATENCY = 2
    DEFAULT_TTL = 6

    def __init__(
            self, album_key: str = ALBUM_KEY,
            latency: float = DEFAULT_LATENCY,
            ttl: float = DEFAULT_TTL,
    ) -> None:
        self.album_key = album_key
        self.latency = latency
        self.cache: MutableMapping[str, dict[str, Any]] = TTLCache(
            maxsize=10_000, ttl=ttl
        )

    @staticmethod
    def get_content(message: Message) -> tuple[Media, str] | None:
        if message.photo:
            return message.photo[-1], "photo"
        if message.video:
            return message.video, "video"
        if message.audio:
            return message.audio, "audio"
        if message.document:
            return message.document, "document"
        return None

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, dict[str, Any]],
                Awaitable[Any]
            ],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id is not None:
            key = event.media_group_id
            media, content_type = cast(
                tuple[Media, str],
                self.get_content(event)
            )

            if key in self.cache:
                if content_type not in self.cache[key]:
                    self.cache[key][content_type] = [media]
                    return

                self.cache[key]["messages"].append(event)
                self.cache[key][content_type].append(media)
                return

            self.cache[key] = {
                content_type: [media],
                "messages": [event],
                "caption": event.html_text,
            }

            await sleep(self.latency)
            data[self.album_key] = Album.model_validate(
                self.cache[key],
                context={"bot": data["bot"]}
            )

        return await handler(event, data)
