from aiogram import types

from src.database.db_funcs import is_has_role, save_user_or_update_status
from src.utils.consts import Roles
from src.utils.funcs import extract_username


def save_new_user_decor(func):
    """
    Костыльный декоратор, который сохраняет или обновляет пользователей
    при их взаимодействии с ботом.
    """

    async def wrapper(update: types.Message | types.CallbackQuery):
        save_user_or_update_status(
            update.from_user.id, extract_username(update)
        )
        await func(update)

    return wrapper


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


superadmin_required = is_has_role_decor(Roles.SUPERADMIN)
admin_required = is_has_role_decor(Roles.ADMIN)
