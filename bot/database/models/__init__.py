"""Модуль с базой данных."""

from bot.database.models.base_models import AlchemyBaseModel, UserRelatedModel
from bot.database.models.users import User
from bot.database.models.settings import Settings
from bot.database.models.laundries import Laundry
from bot.database.models.menus import Menu
from bot.database.models.roles import Role
from bot.database.models.class_lessons import ClassLessons
from bot.database.models.full_lessons import FullLessons
from bot.database.models.educators_schedules import EducatorsSchedule
from bot.database.models.users_to_roles import users_to_roles


__all__ = (
    "AlchemyBaseModel",
    "UserRelatedModel",
    "User",
    "Settings",
    "Laundry",
    "Menu",
    "Role",
    "ClassLessons",
    "FullLessons",
    "EducatorsSchedule",
    "users_to_roles",
)
