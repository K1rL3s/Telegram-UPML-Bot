from aiogram import Router

from bot.handlers.client.cafe_menu import handlers as cafe_menu_handlers
from bot.handlers.client.educators import handlers as educators_handlers
from bot.handlers.client.electives import handlers as electives_handlers
from bot.handlers.client.enrollee import handlers as enrollee_handlers
from bot.handlers.client.laundry import handlers as laundry_handlers
from bot.handlers.client.lessons import handlers as lessons_handlers
from bot.handlers.client.olymps import handlers as olymps_handlers
from bot.handlers.client.settings import handlers as settings_handlers
from bot.handlers.client.start import handlers as start_handlers
from bot.handlers.client.state_cancel.handlers import router as cancel_state_router
from bot.handlers.client.univers import handlers as univers_handlers

client_router = Router()

client_router.include_routers(
    start_handlers.router,
    cafe_menu_handlers.router,
    educators_handlers.router,
    electives_handlers.router,
    laundry_handlers.router,
    lessons_handlers.router,
    enrollee_handlers.router,
    olymps_handlers.router,
    univers_handlers.router,
    settings_handlers.router,
)

__all__ = (
    "cancel_state_router",
    "client_router",
)
