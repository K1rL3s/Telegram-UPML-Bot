from aiogram.fsm.state import State, StatesGroup


class EditingSettings(StatesGroup):
    """Пользовательское состояние для редактирования настроек, требующих ввода."""

    writing = State()


class EditingMenu(StatesGroup):
    """Админские состояния для редактирования приёмов пищи."""

    choose_date = State()
    choose_meal = State()
    writing = State()


class EditingEducators(StatesGroup):
    """Админские состояния для редактирования расписания воспитателей."""

    choose_date = State()
    writing = State()


class EditingLessons(StatesGroup):
    """Админское состояние для отправки расписания уроков."""

    input_images = State()
    all_good = State()
    something_bad = State()
    choose_grade = State()
    choose_date = State()
    confirm = State()


class EditingRoles(StatesGroup):
    """Админские состояния для добавляения нового админа."""

    username = State()
    action = State()
    roles = State()
    confirm = State()


class DoingNotify(StatesGroup):
    """Админское состояние для отправки уведомления."""

    writing = State()
