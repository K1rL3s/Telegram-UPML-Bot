from aiogram.fsm.state import State, StatesGroup


class EditingMenu(StatesGroup):
    choose_date = State()
    choose_meal = State()
    writing = State()


class EditingEducators(StatesGroup):
    choose_date = State()
    writing = State()


class LoadingLessons(StatesGroup):
    image = State()


class AddingNewAdmin(StatesGroup):
    username = State()
    confirm = State()


class DoNotify(StatesGroup):
    writing = State()


class EditingSettings(StatesGroup):
    writing = State()
