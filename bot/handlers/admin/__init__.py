"""
Создание общего роутера для админских обработчиков
чтобы избежать добавление фильтра IsAdmin в каждый файл.
"""

from aiogram import Router

from bot.filters.roles import HasAnyRole
from bot.handlers.admin.cafe_menu import handlers as cafe_menu_handlers
from bot.handlers.admin.educators import handlers as educators_handlers
from bot.handlers.admin.electives import handlers as electives_handlers
from bot.handlers.admin.lessons import handlers as lessons_handlers
from bot.handlers.admin.manage import handlers as manage_handlers
from bot.handlers.admin.notify import handlers as notify_handlers
from bot.handlers.admin.panel import handlers as panel_handlers

admin_router = Router(name=__name__)
admin_router.message.filter(HasAnyRole())
admin_router.callback_query.filter(HasAnyRole())

admin_router.include_routers(
    panel_handlers.router,
    cafe_menu_handlers.router,
    educators_handlers.router,
    electives_handlers.router,
    manage_handlers.router,
    lessons_handlers.router,
    notify_handlers.router,
)


__all__ = ("admin_router",)
