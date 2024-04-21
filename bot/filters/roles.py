from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from shared.database.repository.repository import Repository
from shared.utils.enums import RoleEnum


class RoleAccess(Filter):
    """Фильтр доступа к обработчику по роли (уровню доступа)."""

    def __init__(self, roles: "list[Union[RoleEnum, str]]") -> None:
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
        super().__init__([RoleEnum.SUPERADMIN])


class IsAdmin(RoleAccess):
    """Фильтр по ролям SUPERADMIN и ADMIN."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN])


class HasAnyRole(RoleAccess):
    """Фильтр доступа к админ-панели. Любой, у кого есть роль - имеет доступ."""

    def __init__(self) -> None:
        super().__init__(RoleEnum.all_roles())


class HasNotifyRole(RoleAccess):
    """Фильтр доступа к рассылке уведомлений."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.NOTIFY])


class HasLessonsRole(RoleAccess):
    """Фильтр доступа к редактированию уроков."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.LESSONS])


class HasCafeMenuRole(RoleAccess):
    """Фильтр доступа к редактированию расписаний столовой."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.CAFE_MENU])


class HasEducatorsRole(RoleAccess):
    """Фильтр доступа к редактированию расписаний воспитателей."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.EDUCATORS])


class HasUniversRole(RoleAccess):
    """Фильтр доступа к редактированию информации о вузах."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.UNIVERS])


class HasOlympsRole(RoleAccess):
    """Фильтр доступа к редактированию информации об олимпиадах."""

    def __init__(self) -> None:
        super().__init__([RoleEnum.SUPERADMIN, RoleEnum.ADMIN, RoleEnum.OLYMPS])
