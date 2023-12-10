from aiogram import Router

from bot.handlers.client import (
    cafe_menu,
    educators,
    electives,
    laundry,
    lessons,
    settings,
    start,
)
from bot.handlers.client.state import router as cancel_state_router

client_router = Router()

client_router.include_routers(
    start.router,
    cafe_menu.router,
    educators.router,
    electives.router,
    laundry.router,
    lessons.router,
    settings.router,
)

__all__ = (
    "cancel_state_router",
    "client_router",
)
