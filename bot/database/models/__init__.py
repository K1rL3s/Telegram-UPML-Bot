"""
Модуль с базой данных.
"""
from .base_models import BaseModel, UserRelatedModel
from .users import User
from .settings import Settings
from .laundries import Laundry
from .menus import Menu
from .roles import Role
from .class_lessons import ClassLessons
from .full_lessons import FullLessons
from .educators_schedules import EducatorsSchedule
from .users_to_roles import users_to_roles


__all__ = [
    "BaseModel",
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
]
