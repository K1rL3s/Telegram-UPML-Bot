"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from src.view.cafe_menu import register_cafe_menu_view
from src.view.start import register_base_view


def register_view(dp: Dispatcher) -> None:
    register_base_view(dp)
    register_cafe_menu_view(dp)
