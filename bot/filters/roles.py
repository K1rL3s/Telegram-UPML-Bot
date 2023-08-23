from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from bot.database.repository.repository import Repository
from bot.database.db_session import get_session
from bot.utils.consts import Roles


class RoleAccess(Filter):
    def __init__(self, roles: list[Roles] | tuple[Roles, ...]) -> None:
        self.roles = roles

    # idk how to pass repo in __init__ or __call__ :(
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        async with get_session() as session:
            repo = Repository(session)
            result = await repo.user.is_has_any_role(event.from_user.id, self.roles)
        return result


class IsAdmin(RoleAccess):
    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN])


class IsSuperAdmin(RoleAccess):
    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN])
