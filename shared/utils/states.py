from aiogram.fsm.state import State, StatesGroup


class EditingSettings(StatesGroup):
    """Пользовательское состояние для редактирования настроек, требующих ввода."""

    write = State()


class EditingMenu(StatesGroup):
    """Админские состояния для редактирования приёмов пищи."""

    choose_date = State()
    choose_meal = State()
    write = State()


class EditingEducators(StatesGroup):
    """Админские состояния для редактирования расписания воспитателей."""

    choose_date = State()
    write = State()


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
    choose_user = State()  # Если никнеймы совпадают, то админ попадает сюда
    roles = State()
    confirm = State()


class DoingNotify(StatesGroup):
    """Админское состояние для отправки уведомления."""

    write = State()


class AddingUniver(StatesGroup):
    """Админское состояние для добавление вуза."""

    city = State()
    title = State()
    description = State()
    confirm = State()


class AddingOlymp(StatesGroup):
    """Админское состояние для добавление олимпиады."""

    subject = State()
    title = State()
    description = State()
    confirm = State()


class DeletingUniver(StatesGroup):
    """Админское состояние для удаления вуза."""

    confirm = State()


class DeletingOlymp(StatesGroup):
    """Админское состояние для удаления олимпиады."""

    confirm = State()
