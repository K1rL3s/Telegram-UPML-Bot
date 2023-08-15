"""
Хранилище клавиатур.
"""

from bot.keyboards.universal import cancel_state_keyboard
from bot.keyboards.start import go_to_main_menu_keyboard, main_menu_keyboard
from bot.keyboards.cafe_menu import cafe_menu_keyboard
from bot.keyboards.educators import educators_keyboard
from bot.keyboards.lessons import lessons_keyboard
from bot.keyboards.settings import settings_keyboard, choose_grade_keyboard
from bot.keyboards.admin.admin_notifies import (
    notify_panel_keyboard,
    notify_for_grade_keyboard,
    notify_for_class_keyboard,
    notify_confirm_keyboard,
)
from bot.keyboards.admin.admin import (
    admin_panel_keyboard,
)
from bot.keyboards.admin.admin_updates import (
    choose_meal_keyboard,
    confirm_edit_keyboard,
)
from bot.keyboards.admin.admin_manage import (
    add_new_admin_sure_keyboard,
    admins_list_keyboard,
    check_admin_keyboard,
)
from bot.keyboards.laundry import laundry_keyboard
