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
from bot.handlers import start
from bot.handlers import settings
from bot.handlers import lessons
from bot.handlers import cafe_menu
from bot.handlers import laundry
from bot.handlers import educators
from bot.handlers import electives
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
