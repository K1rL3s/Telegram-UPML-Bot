from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.database.db_funcs import (
    add_role_to_user, get_user_id_by_username, get_users_with_role,
    remove_role_from_user,
)
from src.keyboards import (
    admins_list_keyboard, cancel_state_keyboard,
    check_admin_keyboard,
)
from src.keyboards.admin import (
    add_new_admin_sure_keyboard,
    admin_menu_keyboard,
)
from src.utils.consts import CallbackData, Roles
from src.utils.decorators import superadmin_required
from src.utils.funcs import username_by_user_id
from src.utils.states import AddingNewAdmin


@superadmin_required
async def admins_list_view(callback: types.CallbackQuery, *_, **__) -> None:
    page = int(
        callback.data.replace(
            CallbackData.OPEN_ADMINS_LIST_PAGE_, ''
        ) or 0
    )

    admins = [
        (await username_by_user_id(user.user_id), user.user_id)
        for user in get_users_with_role(Roles.ADMIN)
    ]

    keyboard = admins_list_keyboard(admins, page)
    text = 'Список админов:'

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@superadmin_required
async def admin_add_view(callback: types.CallbackQuery, *_, **__) -> None:
    await AddingNewAdmin.username.set()
    text = 'Введите имя пользователя, которого хотите сделать админом.'
    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@superadmin_required
async def admin_add_check_username_view(
        message: types.Message | types.CallbackQuery,
        state: FSMContext, *_, **__
) -> None:
    username = message.text
    user_id = get_user_id_by_username(username)

    if user_id is None:
        text = 'Не могу найти у себя такого пользователя.'
        await message.reply(
            text=text,
            reply_markup=cancel_state_keyboard
        )
        return

    async with state.proxy() as data:
        data['user_id'] = user_id

    await AddingNewAdmin.confirm.set()
    text = f'Добавить в админы [{username}](tg://user?id={user_id})?'
    await message.reply(
        text=text,
        reply_markup=add_new_admin_sure_keyboard
    )


@superadmin_required
async def admin_add_confirm_view(
        callback: types.CallbackQuery, state: FSMContext, *_, **__
) -> None:
    async with state.proxy() as data:
        user_id = data['user_id']
        add_role_to_user(user_id, Roles.ADMIN)
        text = 'Успешно!'
        await callback.message.edit_text(
            text=text,
            reply_markup=admin_menu_keyboard(callback.from_user.id)
        )
        await state.finish()


@superadmin_required
async def admin_check_view(callback: types.CallbackQuery, *_, **__) -> None:
    user_id, page = map(
        int,
        callback.data.replace(
            CallbackData.CHECK_ADMIN_, ''
        ).split('_')
    )
    text = f"Админ " \
           f"[{await username_by_user_id(user_id)}](tg://user?id={user_id})"
    keyboard = check_admin_keyboard(user_id, page, sure=False)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@superadmin_required
async def admin_remove_view(callback: types.CallbackQuery, *_, **__) -> None:
    if callback.data.startswith(CallbackData.REMOVE_ADMIN_SURE_):
        user_id = int(
            callback.data.replace(
                CallbackData.REMOVE_ADMIN_SURE_, ''
            )
        )
        remove_role_from_user(user_id, Roles.ADMIN)
        callback.data = CallbackData.OPEN_ADMINS_LIST_PAGE_
        await admins_list_view(callback)
        return

    user_id, page = map(
        int, callback.data.replace(
            CallbackData.REMOVE_ADMIN_, ''
        ).split('_')
    )

    text = f"Вы точно хотите удалить из админов" \
           f" [{await username_by_user_id(user_id)}](tg://user?id={user_id})?"
    keyboard = check_admin_keyboard(user_id, page, sure=True)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


def register_admin_manage_view(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        admins_list_view,
        lambda callback: callback.data.startswith(
            CallbackData.OPEN_ADMINS_LIST_PAGE_
        )
    )
    dp.register_callback_query_handler(
        admin_add_view,
        text=CallbackData.ADD_NEW_ADMIN
    )
    dp.register_message_handler(
        admin_add_check_username_view,
        state=AddingNewAdmin.username
    )
    dp.register_callback_query_handler(
        admin_add_confirm_view,
        text=CallbackData.ADD_NEW_ADMIN_SURE,
        state=AddingNewAdmin.confirm
    )
    dp.register_callback_query_handler(
        admin_check_view,
        lambda callback: callback.data.startswith(
            CallbackData.CHECK_ADMIN_
        )
    )
    dp.register_callback_query_handler(
        admin_remove_view,
        lambda callback: callback.data.startswith(
            CallbackData.REMOVE_ADMIN_
        )
    )
