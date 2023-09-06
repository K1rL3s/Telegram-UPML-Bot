"""View-часть, передающая события в logic-часть."""

from typing import TYPE_CHECKING

from bot.handlers.admin import (
    admin,
    admin_cafe_menu,
    admin_educators,
    admin_electives,
    admin_lessons,
    admin_manage,
    admin_notifies,
)
from bot.handlers.client import (
    cafe_menu,
    educators,
    electives,
    laundry,
    lessons,
    settings,
    start,
)
from bot.handlers import errors

if TYPE_CHECKING:
    from aiogram import Dispatcher


__all__ = [
    "include_routers",
]


def include_routers(dp: "Dispatcher") -> None:
    """Включение роутов в главный dispatcher."""
    dp.include_routers(
        start.router,
        settings.router,
        lessons.router,
        cafe_menu.router,
        laundry.router,
        educators.router,
        electives.router,
        admin.router,
        admin_cafe_menu.router,
        admin_educators.router,
        admin_electives.router,
        admin_lessons.router,
        admin_manage.router,
        admin_notifies.router,
        errors.router,
    )
