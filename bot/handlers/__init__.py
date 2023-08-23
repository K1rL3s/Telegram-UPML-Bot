"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from bot.handlers.admin import (
    admin_cafe_menu,
    admin_educators,
    admin_electives,
    admin_lessons,
    admin_manage,
    admin_notifies,
)
from bot.handlers.client import (
    start,
    settings,
    lessons,
    cafe_menu,
    laundry,
    educators,
    electives,
)
from bot.handlers import errors


__all__ = [
    "include_routers",
]


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
            admin_cafe_menu.router,
            admin_educators.router,
            admin_electives.router,
            admin_lessons.router,
            admin_manage.router,
            admin_notifies.router,
            errors.router,
        )
    )
