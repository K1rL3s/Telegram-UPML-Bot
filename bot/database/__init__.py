"""
Модуль с базой данных.
"""
from .models.base_models import BaseModel, UserRelatedModel
from .models.menus import Menu
from .models.users import User
from .models.full_lessons import FullLessons
from .models.class_lessons import ClassLessons
from .models.roles import Role
from .models.laundries import Laundry
from .models.settings import Settings
from .models.users_to_roles import users_to_roles