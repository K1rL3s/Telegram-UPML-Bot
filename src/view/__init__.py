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
from src.view.errors import register_errors
from src.view.start import register_start_view
from src.view.cafe_menu import register_cafe_menu_view
from src.view.lessons import register_lessons_view
from src.view.settings import register_setings_view


def register_view(dp: Dispatcher) -> None:
    register_start_view(dp)
    register_cafe_menu_view(dp)
    register_lessons_view(dp)
    register_setings_view(dp)
    register_admin_updates_view(dp)
    register_admin_manage_view(dp)
    register_admin_notifies_view(dp)
    register_errors(dp)
