from aiogram.filters.callback_data import CallbackData


class Paginator(CallbackData, prefix="paginate"):
    menu: str
    page: int
