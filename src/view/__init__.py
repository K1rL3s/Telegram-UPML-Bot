"""
Модуль, отвечающий за приём сообщений из телеги,
передачи их в функцию-обработчик и возврат ответа.
"""

from aiogram import Dispatcher

from src.view.start import register_start_view


def register_view(dp: Dispatcher) -> None:
    register_start_view(dp)
