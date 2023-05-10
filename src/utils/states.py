# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class LoadingLessons(StatesGroup):
    image = State()


class AddingNewAdmin(StatesGroup):
    username = State()
    confirm = State()
