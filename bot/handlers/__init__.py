"""View-часть, передающая события в logic-часть."""

from typing import TYPE_CHECKING

from bot.handlers import errors
from bot.handlers.admin import admin_router
from bot.handlers.client import cancel_state_router, client_router

if TYPE_CHECKING:
    from aiogram import Dispatcher


__all__ = ("include_routers",)


def include_routers(dp: "Dispatcher") -> None:
    """Включение роутов в главный dispatcher."""
    dp.include_routers(
        client_router,
        admin_router,
        cancel_state_router,
        errors.router,
    )
