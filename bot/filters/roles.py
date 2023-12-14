from typing import TYPE_CHECKING, Union

from aiogram.filters import Filter

from shared.utils.enums import Roles

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from shared.database.repository.repository import Repository


class RoleAccess(Filter):
    """Фильтр доступа к обработчику по роли (уровню доступа)."""

    def __init__(self, roles: "list[Union[Roles, str]]") -> None:
        self.roles = roles

    async def __call__(
        self,
        event: "Union[Message, CallbackQuery]",
        repo: "Repository",
    ) -> bool:
        return await repo.user.is_has_any_role(event.from_user.id, self.roles)


class IsSuperAdmin(RoleAccess):
    """Фильтр по роли SUPERADMIN."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN])


class IsAdmin(RoleAccess):
    """Фильтр по ролям SUPERADMIN и ADMIN."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN])


class HasAnyRole(RoleAccess):
    """Фильтр доступа к админ-панели. Любой, у кого есть роль - имеет доступ."""

    def __init__(self) -> None:
        super().__init__(Roles.all_roles())


class HasNotifyRole(RoleAccess):
    """Фильтр доступа к рассылке уведомлений."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN, Roles.NOTIFY])


class HasLessonsRole(RoleAccess):
    """Фильтр доступа к редактированию уроков."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN, Roles.LESSONS])


class HasCafeMenuRole(RoleAccess):
    """Фильтр доступа к редактированию расписаний столовой."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN, Roles.CAFE_MENU])


class HasEducatorsRole(RoleAccess):
    """Фильтр доступа к редактированию расписаний воспитателей."""

    def __init__(self) -> None:
        super().__init__([Roles.SUPERADMIN, Roles.ADMIN, Roles.EDUCATORS])
