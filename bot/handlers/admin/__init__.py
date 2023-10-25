"""
Создание общего роутера для админских обработчиков.

Избегаю добавление фильтра IsAdmin в каждый обработчик.
"""

from aiogram import Router

from bot.filters.roles import HasAnyRole

from bot.handlers.admin import (
    cafe_menu,
    educators,
    electives,
    lessons,
    manage,
    notifies,
    panel,
)


admin_router = Router(name=__name__)
admin_router.message.filter(HasAnyRole())
admin_router.callback_query.filter(HasAnyRole())

admin_router.include_routers(
    panel.router,
    cafe_menu.router,
    educators.router,
    electives.router,
    manage.router,
    lessons.router,
    notifies.router,
)


__all__ = ("admin_router",)
