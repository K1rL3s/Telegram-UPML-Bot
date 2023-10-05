"""
Создание общего роутера для админских обработчиков.

Избегаю добавление фильтра IsAdmin в каждый обработчик.
"""

from aiogram import Router

from bot.filters import IsAdmin, IsSuperAdmin

from bot.handlers.admin import (
    admin,
    cafe_menu,
    educators,
    electives,
    lessons,
    manage,
    notifies,
)


admin_router = Router(name=__name__)
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())

__super_admin_router = Router(name=__name__)
__super_admin_router.message.filter(IsSuperAdmin())
__super_admin_router.callback_query.filter(IsSuperAdmin())

__super_admin_router.include_routers(
    manage.router,
)

admin_router.include_routers(
    admin.router,
    cafe_menu.router,
    educators.router,
    electives.router,
    lessons.router,
    notifies.router,
    __super_admin_router,
)
