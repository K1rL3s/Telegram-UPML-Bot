from aiogram.filters.callback_data import CallbackData as AiogramCallbackData


class Callback(AiogramCallbackData):
    data: str


class CallbackData:
    OPEN_MAIN_MENU = Callback(data='open_main_menu').pack()
    OPEN_SETTINGS = Callback(data='open_settings')
    OPEN_LAUNDRY = Callback(data='open_laundry')
    OPEN_EDUCATORS = Callback(data='open_educators')
    OPEN_ELECTIVES = Callback(data='open_electives')
    OPEN_ADMIN_PANEL = Callback(data='open_admin_panel')
    OPEN_CAFE_MENU_ON_ = Callback(data='open_cafe_menu_on_')
    OPEN_CAFE_MENU_TODAY = Callback(data=OPEN_CAFE_MENU_ON_ + 'today')
    OPEN_LESSONS_ON_ = Callback(data='open_lessons_on_')
    OPEN_LESSONS_TODAY = Callback(data=OPEN_LESSONS_ON_ + 'today')

    CHANGE_GRADE_TO_ = Callback(data='edit_grade_to_')
    PREFIX_SWITCH = Callback(data='switch_')
    SWITCH_LESSONS_NOTIFY = Callback(data=PREFIX_SWITCH + 'lessons_notify')
    SWITCH_NEWS_NOTIFY = Callback(data=PREFIX_SWITCH + 'news_notify')
    EDIT_SETTINGS_PREFIX = Callback(data='edit_settings_')
    EDIT_WASHING_TIME = Callback(data=EDIT_SETTINGS_PREFIX + 'washing_time')
    EDIT_DRYING_TIME = Callback(data=EDIT_SETTINGS_PREFIX + 'drying_time')

    CANCEL_STATE = Callback(data='cancel_state')

    AUTO_UPDATE_CAFE_MENU = Callback(data='auto_update_cafe_menu')
    EDIT_CAFE_MENU = Callback(data='edit_cafe_menu')
    EDIT_BREAKFAST = Callback(data='edit_breakfast')
    EDIT_LUNCH = Callback(data='edit_lunch')
    EDIT_DINNER = Callback(data='edit_dinner')
    EDIT_SNACK = Callback(data='edit_snack')
    EDIT_SUPPER = Callback(data='edit_supper')
    EDIT_CONFIRM = Callback(data='edit_cafe_menu_confirm')

    UPLOAD_LESSONS = Callback(data='upload_lessons')

    DO_A_NOTIFY_FOR_ = Callback(data='do_a_notify_for_')
    FOR_ALL = Callback(data=DO_A_NOTIFY_FOR_ + 'all')
    FOR_GRADE = Callback(data=DO_A_NOTIFY_FOR_ + 'grade')
    FOR_CLASS = Callback(data=DO_A_NOTIFY_FOR_ + 'class')
    NOTIFY_CONFIRM = Callback(data='notify_confirm')

    OPEN_ADMINS_LIST_PAGE_ = Callback(data='open_admins_list_page_')
    CHECK_ADMIN_ = Callback(data='check_admin_')
    REMOVE_ADMIN_ = Callback(data='remove_admin_')
    REMOVE_ADMIN_SURE_ = Callback(data='remove_admin_sure_')
    ADD_NEW_ADMIN = Callback(data='add_new_admin')
    ADD_NEW_ADMIN_SURE = Callback(data='add_new_admin_sure')

    START_LAUNDRY_PREFIX = Callback(data='start_laundry_')
    START_WASHING_TIMER = Callback(data=START_LAUNDRY_PREFIX + 'washing_time')
    START_DRYING_TIMER = Callback(data=START_LAUNDRY_PREFIX + 'drying_time')
    CANCEL_LAUNDRY_TIMER = Callback(data='cancel_laundry_timer')