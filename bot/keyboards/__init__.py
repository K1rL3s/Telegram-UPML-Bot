"""
Хранилище клавиатур.
"""

from bot.keyboards.universal import cancel_state_keyboard
from bot.keyboards.client.laundry import laundry_keyboard
from bot.keyboards.client.cafe_menu import cafe_menu_keyboard
from bot.keyboards.client.educators import educators_keyboard
from bot.keyboards.client.lessons import lessons_keyboard
from bot.keyboards.client.start import (
    go_to_main_menu_keyboard,
    start_reply_keyboard,
    main_menu_inline_keyboard,
)
from bot.keyboards.client.settings import (
    settings_keyboard,
    choose_grade_keyboard,
)
from bot.keyboards.admin.admin_notifies import (
    notify_panel_keyboard,
    notify_for_grade_keyboard,
    notify_for_class_keyboard,
    notify_confirm_keyboard,
)
from bot.keyboards.admin.admin import admin_panel_keyboard
from bot.keyboards.admin.admin_updates import (
    choose_meal_keyboard,
    confirm_edit_keyboard,
)
from bot.keyboards.admin.admin_manage import (
    add_new_admin_sure_keyboard,
    admins_list_keyboard,
    check_admin_keyboard,
)


__all__ = [
    "cancel_state_keyboard",
    "laundry_keyboard",
    "cafe_menu_keyboard",
    "educators_keyboard",
    "lessons_keyboard",
    "go_to_main_menu_keyboard",
    "start_reply_keyboard",
    "main_menu_inline_keyboard",
    "settings_keyboard",
    "choose_grade_keyboard",
    "notify_panel_keyboard",
    "notify_for_grade_keyboard",
    "notify_for_class_keyboard",
    "notify_confirm_keyboard",
    "admin_panel_keyboard",
    "choose_meal_keyboard",
    "confirm_edit_keyboard",
    "add_new_admin_sure_keyboard",
    "admins_list_keyboard",
    "check_admin_keyboard",
]
