# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class CafeMenuStates(StatesGroup):
    watching = State()
