"""
Source:
https://github.com/aiogram/aiogram
https://docs.aiogram.dev/en/dev-3.x/api/session/middleware.html

This file is part of the aiogram project.
Licensed under the MIT License;
you may not use this file except in compliance with the License.
"""

import asyncio

from aiogram import Bot
from aiogram.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from aiogram.dispatcher.dispatcher import DEFAULT_BACKOFF_CONFIG
from aiogram.exceptions import (
    TelegramRetryAfter,
    TelegramServerError,
    TelegramNetworkError,
)
from aiogram.methods import TelegramMethod, Response
from aiogram.methods.base import TelegramType
from aiogram.utils.backoff import BackoffConfig, Backoff
from loguru import logger


class RetryRequestMiddleware(BaseRequestMiddleware):
    def __init__(
        self,
        backoff_config: BackoffConfig = DEFAULT_BACKOFF_CONFIG,
    ) -> None:
        self.backoff_config = backoff_config

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        backoff = Backoff(config=self.backoff_config)

        while True:
            try:
                return await make_request(bot, method)
            except TelegramRetryAfter as e:
                logger.error(
                    f"Request '{type(method).__name__}' "
                    f"failed due to rate limit. Sleeping {e.retry_after}"
                )
                backoff.reset()
                await asyncio.sleep(e.retry_after)
            except (TelegramServerError, TelegramNetworkError) as e:
                logger.error(
                    f"Request '{type(method).__name__}' "
                    f"failed due to {type(e).__name__} - {e}. "
                    f"Sleeping {backoff.next_delay}"
                )
                await backoff.asleep()
