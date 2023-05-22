"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from src.view.admin import (
    register_admin_manage_view,
    register_admin_updates_view,
    register_admin_notifies_view,
)
from src.view.start import register_start_view
from src.view.cafe_menu import register_cafe_menu_view
from src.view.lessons import register_lessons_view
from src.view.laundry import register_laundry_view
from src.view.educators import register_educators_view
from src.view.electives import register_electives_view
from src.view.settings import register_setings_view
from src.view.errors import register_errors


def register_view(dp: Dispatcher) -> None:
    registers = (
        register_start_view,
        register_cafe_menu_view,
        register_lessons_view,
        register_laundry_view,
        register_educators_view,
        register_electives_view,
        register_setings_view,
        register_admin_updates_view,
        register_admin_manage_view,
        register_admin_notifies_view,
        register_errors,
    )
    for register in registers:
        register(dp)
