from typing import TYPE_CHECKING, Union

from aiogram.filters import Filter

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.utils.enums import Roles


if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message


class RoleAccess(Filter):
    """Фильтр доступа к обработчику по роли (уровню доступа)."""

    def __init__(self, roles: list["Roles"]) -> None:
        self.roles = roles

    # idk how to pass repo in __init__ or __call__ :(
    async def __call__(self, event: "Union[Message, CallbackQuery]") -> bool:
        async with get_session() as session:
            repo = Repository(session)
            return await repo.user.is_has_any_role(event.from_user.id, self.roles)


class IsAdmin(RoleAccess):
    """Фильтр по ролям SUPERADMIN и ADMIN."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN])


class IsSuperAdmin(RoleAccess):
    """Фильтр по роли SUPERADMIN."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN])
