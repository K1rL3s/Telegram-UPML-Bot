"""Модуль с базой данных."""

from shared.database import AlchemyBaseModel, UserRelatedModel
from shared.database.models.class_lessons import ClassLessons
from shared.database.models.educators_schedules import EducatorsSchedule
from shared.database.models.full_lessons import FullLessons
from shared.database.models.laundries import Laundry
from shared.database.models.menus import Menu
from shared.database.models.olymps import Olymp
from shared.database.models.roles import Role
from shared.database.models.settings import Settings
from shared.database.models.univers import Univer
from shared.database.models.users import User
from shared.database.models.users_to_roles import UsersToRoles

__all__ = (
    "AlchemyBaseModel",
    "UserRelatedModel",
    "User",
    "Settings",
    "Laundry",
    "Menu",
    "Olymp",
    "Role",
    "ClassLessons",
    "FullLessons",
    "EducatorsSchedule",
    "UsersToRoles",
    "Univer",
)
