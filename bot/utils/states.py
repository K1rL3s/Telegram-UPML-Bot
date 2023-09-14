from aiogram.fsm.state import State, StatesGroup


class EditingMenu(StatesGroup):
    """Админские состояния для редактирования приёмов пищи."""

    choose_date = State()
    choose_meal = State()
    writing = State()


class EditingEducators(StatesGroup):
    """Админские состояния для редактирования расписания воспитателей."""

    choose_date = State()
    writing = State()


class LoadingLessons(StatesGroup):
    """Админское состояние для отправки расписания уроков."""

    image = State()
    all_good = State()
    something_bad = State()
    choose_grade = State()
    choose_date = State()
    confirm = State()


class AddingNewAdmin(StatesGroup):
    """Админские состояния для добавляения нового админа."""

    username = State()
    confirm = State()


class DoNotify(StatesGroup):
    """Админское состояние для отправки уведомления."""

    writing = State()


class EditingSettings(StatesGroup):
    """Пользовательское состояние для редактирования настроек, требующий ввода."""

    writing = State()
