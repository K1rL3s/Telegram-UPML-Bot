# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class EditingMenu(StatesGroup):
    choose_date = State()
    choose_meal = State()
    editing = State()


class LoadingLessons(StatesGroup):
    image = State()


class AddingNewAdmin(StatesGroup):
    username = State()
    confirm = State()
