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


client_router = Router()

client_router.include_routers(
    cafe_menu.router,
    educators.router,
    electives.router,
    laundry.router,
    lessons.router,
    settings.router,
    start.router,
)
