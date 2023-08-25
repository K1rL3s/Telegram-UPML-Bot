"""
This file is part of the aiogram project.

Licensed under the MIT License;
you may not use this file except in compliance with the License.

Source:
https://github.com/aiogram/aiogram
https://docs.aiogram.dev/en/dev-3.x/api/session/middleware.html
"""

import asyncio
from typing import TYPE_CHECKING

from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.dispatcher.dispatcher import DEFAULT_BACKOFF_CONFIG
from aiogram.exceptions import (
    TelegramNetworkError,
    TelegramRetryAfter,
    TelegramServerError,
)
from aiogram.utils.backoff import Backoff, BackoffConfig
from loguru import logger

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.methods import Response, TelegramMethod
    from aiogram.methods.base import TelegramType
    from aiogram.client.session.middlewares.base import NextRequestMiddlewareType


class RetryRequestMiddleware(BaseRequestMiddleware):
    """Мидлварь на запросы к апи телеграма."""

    def __init__(
        self,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
    ) -> None:
        self.backoff_config = backoff_config

    async def __call__(
        self,
        make_request: "NextRequestMiddlewareType[TelegramType]",
        bot: "Bot",
        method: "TelegramMethod[TelegramType]",
    ) -> "Response[TelegramType]":
        backoff = Backoff(config=self.backoff_config)

        while True:
            try:
                return await make_request(bot, method)
            except TelegramRetryAfter as e:
                logger.error(
                    f"Request '{type(method).__name__}' "
                    f"failed due to rate limit. Sleeping {e.retry_after}",
                )
                backoff.reset()
                await asyncio.sleep(e.retry_after)
            except (TelegramServerError, TelegramNetworkError) as e:
                logger.error(
                    f"Request '{type(method).__name__}' "
                    f"failed due to {type(e).__name__} - {e}. "
                    f"Sleeping {backoff.next_delay}",
                )
                await backoff.asleep()
