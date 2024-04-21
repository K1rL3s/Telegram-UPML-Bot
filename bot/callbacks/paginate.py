from collections.abc import Callable
from typing import Any

from aiogram.filters.callback_data import CallbackData, T


class Paginator(CallbackData, prefix="paginator"):
    menu: str
    page: int

    @classmethod
    def init_wrapper(cls: type[T], **data: Any) -> Callable[..., T]:
        def wrapped_init(**kwargs):
            return cls(**kwargs, **data)

        return wrapped_init


class OlympsPaginator(Paginator, prefix="olymps_paginator"):
    subject: str


class UniversPaginator(Paginator, prefix="univers_paginator"):
    city: str
