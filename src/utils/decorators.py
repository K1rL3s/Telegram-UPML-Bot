from aiogram import types

from src.database.db_funcs import is_has_role
from src.utils.consts import Roles


# Подумать над костылём в функциях (*_, *__)
# из-за передачи всех аргументов
def is_has_role_decor(role: Roles | str):
    """
    Декоратор, дающий доступ к команде только имеющим роль.
    """

    def decorator(func):

        async def wrapper(
                update: types.Message | types.CallbackQuery,
                *args,
                **kwargs
        ):
            if is_has_role(update.from_user.id, role):
                await func(update, *args, **kwargs)

        return wrapper

    return decorator


admin_required = is_has_role_decor(Roles.ADMIN)
