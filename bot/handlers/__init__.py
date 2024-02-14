"""View-часть, передающая события в logic-часть."""

from aiogram import Dispatcher

from ..handlers import errors
from .admin import admin_router
from .client import cancel_state_router, client_router

__all__ = ("include_routers",)


def include_routers(dp: "Dispatcher") -> None:
    """Включение роутов в главный dispatcher."""
    dp.include_routers(
        client_router,
        admin_router,
        cancel_state_router,
        errors.router,
    )
