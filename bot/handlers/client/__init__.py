from aiogram import Router

from .cafe_menu import handlers as cafe_menu_handlers
from .educators import handlers as educators_handlers
from .electives import handlers as electives_handlers
from .enrollee import handlers as enrollee_handlers
from .laundry import handlers as laundry_handlers
from .lessons import handlers as lessons_handlers
from .olymps import handlers as olymps_handlers
from .settings import handlers as settings_handlers
from .start import handlers as start_handlers
from .state_cancel.handlers import router as cancel_state_router
from .univers import handlers as univers_handlers

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
