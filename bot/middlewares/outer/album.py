"""Source: https://github.com/wakaree/simple_echo_bot."""

from asyncio import sleep
from typing import TYPE_CHECKING, Any, Final

from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from bot.middlewares.base import BaseInfoMiddleware
from bot.types import Album, Media

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, MutableMapping


ALBUM_KEY: Final[str] = "album"


class AlbumsMiddleware(BaseInfoMiddleware):
    """Мидлварь для обработки группы сообщений с файлами (альбомом)."""

    DEFAULT_LATENCY = 1
    DEFAULT_TTL = 2

    def __init__(
        self,
        album_key: str = ALBUM_KEY,
        latency: float = DEFAULT_LATENCY,
        ttl: float = DEFAULT_TTL,
    ) -> None:
        self.album_key = album_key
        self.latency = latency
        self.cache: MutableMapping[str, dict[str, Any]] = TTLCache(
            maxsize=10_000,
            ttl=ttl,
        )

    @staticmethod
    def _get_content(message: Message) -> tuple["Media", str]:
        """Файл и тип медиа из сообщения."""
        if message.photo:
            return message.photo[-1], "photo"
        if message.video:
            return message.video, "video"
        if message.audio:
            return message.audio, "audio"
        if message.document:
            return message.document, "document"
        raise RuntimeError("Update middleware before using. Unknown file type found.")

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: "TelegramObject",
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id is not None:
            key = event.media_group_id
            media, content_type = self._get_content(event)

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
                context={"bot": data["bot"]},
            )

        return await handler(event, data)
