"""
Создание общего роутера для админских обработчиков.

Избегаю добавление фильтра IsAdmin в каждый обработчик.
"""

from aiogram import Router

from bot.filters import IsAdmin, IsSuperAdmin

from bot.handlers.admin import (
    admin,
    admin_cafe_menu,
    admin_educators,
    admin_electives,
    admin_lessons,
    admin_manage,
    admin_notifies,
)


admin_router = Router(name=__name__)
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())

__super_admin_router = Router(name=__name__)
__super_admin_router.message.filter(IsSuperAdmin())
__super_admin_router.callback_query.filter(IsSuperAdmin())

__super_admin_router.include_routers(
    admin_manage.router,
)

admin_router.include_routers(
    admin.router,
    admin_cafe_menu.router,
    admin_educators.router,
    admin_electives.router,
    admin_lessons.router,
    admin_notifies.router,
    __super_admin_router,
)
