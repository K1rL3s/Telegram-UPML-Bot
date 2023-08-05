"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from src.view.admin import (
    admin_manage_router,
    admin_updates_router,
    admin_notifies_router,
)
from src.view.start import router as start_router
from src.view.settings import router as settings_router
from src.view.lessons import router as lessons_router
from src.view.cafe_menu import router as cafe_menu_router

from src.view.laundry import router as laundry_router
from src.view.educators import router as educators_router
from src.view.electives import router as electives_router
from src.view.errors import router as errors_router


def register_view_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        *(
            start_router,
            settings_router,
            lessons_router,
            cafe_menu_router,
            laundry_router,
            educators_router,
            electives_router,
            admin_updates_router,
            admin_manage_router,
            admin_notifies_router,
            # errors_router,
        )
    )
