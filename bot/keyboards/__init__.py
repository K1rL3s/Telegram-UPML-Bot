"""Хранилище клавиатур."""

from bot.keyboards.admin.admin import admin_panel_keyboard
from bot.keyboards.admin.cafe_menu import choose_meal_keyboard
from bot.keyboards.admin.lessons import choose_parallel_keyboard
from bot.keyboards.admin.manage import (
    admins_list_keyboard,
    check_admin_roles_keyboard,
    edit_roles_keyboard,
    roles_actions_keyboard,
)
from bot.keyboards.admin.notifies import (
    notify_for_class_keyboard,
    notify_for_grade_keyboard,
    notify_menu_keyboard,
)
from bot.keyboards.client.cafe_menu import cafe_menu_keyboard
from bot.keyboards.client.educators import educators_keyboard
from bot.keyboards.client.laundry import laundry_keyboard
from bot.keyboards.client.lessons import lessons_keyboard
from bot.keyboards.client.settings import choose_grade_keyboard, settings_keyboard
from bot.keyboards.client.start import (
    go_to_main_menu_keyboard,
    main_menu_keyboard,
    start_reply_keyboard,
)
from bot.keyboards.universal import cancel_state_keyboard, confirm_cancel_keyboard

__all__ = (
    "admin_panel_keyboard",
    "admins_list_keyboard",
    "cafe_menu_keyboard",
    "cancel_state_keyboard",
    "check_admin_roles_keyboard",
    "choose_grade_keyboard",
    "choose_meal_keyboard",
    "choose_parallel_keyboard",
    "confirm_cancel_keyboard",
    "edit_roles_keyboard",
    "educators_keyboard",
    "go_to_main_menu_keyboard",
    "laundry_keyboard",
    "lessons_keyboard",
    "main_menu_keyboard",
    "notify_for_class_keyboard",
    "notify_for_grade_keyboard",
    "notify_menu_keyboard",
    "roles_actions_keyboard",
    "settings_keyboard",
    "start_reply_keyboard",
)
