"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from bot.handlers.admin import (
    admin_updates,
    admin_manage,
    admin_notifies,
)
from bot.handlers.client import (
    start, settings, lessons, cafe_menu,
    laundry, educators, electives,
)
from bot.handlers import errors


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        *(
            start.router,
            settings.router,
            lessons.router,
            cafe_menu.router,
            laundry.router,
            educators.router,
            electives.router,
            admin_updates.router,
            admin_manage.router,
            admin_notifies.router,
            # errors_router,
        )
    )
