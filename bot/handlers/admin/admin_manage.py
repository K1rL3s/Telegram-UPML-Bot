from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.db_funcs import Repository
from bot.filters import IsSuperAdmin
from bot.keyboards import (
    admins_list_keyboard, cancel_state_keyboard,
    check_admin_keyboard, add_new_admin_sure_keyboard,
    admin_panel_keyboard,
)
from bot.utils.consts import CallbackData, Roles
from bot.utils.funcs import name_link, username_by_user_id
from bot.utils.states import AddingNewAdmin


router = Router(name=__name__)


@router.callback_query(
    F.data.startswith(CallbackData.OPEN_ADMINS_LIST_PAGE_),
    IsSuperAdmin(),
)
async def admins_list_handler(
        callback: types.CallbackQuery,
        repo: Repository,
        callback_data: str = None,
) -> None:
    """
    Обработчик кнопки "Список админов".
    """
    callback_data = callback_data or callback.data
    page = int(
        callback_data.replace(
            CallbackData.OPEN_ADMINS_LIST_PAGE_, ''
        ) or 0
    )

    admins = [
        (await username_by_user_id(callback.bot, user.user_id), user.user_id)
        for user in await repo.get_users_with_role(Roles.ADMIN)
    ]

    keyboard = admins_list_keyboard(admins, page)
    text = 'Список админов:'

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    F.data == CallbackData.ADD_NEW_ADMIN,
    IsSuperAdmin(),
)
async def admin_add_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """
    Обработчик кнопки "Добавить админа".
    """
    await state.set_state(AddingNewAdmin.username)
    text = 'Введите имя пользователя, которого хотите сделать админом.'
    await callback.message.edit_text(
        text=text,
        reply_markup=cancel_state_keyboard
    )


@router.message(
    StateFilter(AddingNewAdmin.username),
    IsSuperAdmin(),
)
async def admin_add_check_username_handler(
        message: types.Message | types.CallbackQuery,
        state: FSMContext,
        repo: Repository,
) -> None:
    """
    Обработчик сообщения с юзернеймом админа, которого хотят добавить.
    """
    username = message.text
    user_id = await repo.get_user_id_by_username(username)

    if user_id is None:
        text = 'Не могу найти у себя такого пользователя.'
        await message.reply(
            text=text,
            reply_markup=cancel_state_keyboard
        )
        return

    await state.update_data(user_id=user_id)
    await state.set_state(AddingNewAdmin.confirm)

    text = f'Добавить в админы {name_link(username, user_id)}?'
    await message.reply(
        text=text,
        reply_markup=add_new_admin_sure_keyboard
    )


@router.callback_query(
    F.data == CallbackData.ADD_NEW_ADMIN_SURE,
    StateFilter(AddingNewAdmin.confirm),
    IsSuperAdmin(),
)
async def admin_add_confirm_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки "Подтвердить" при добавлении админа.
    """
    user_id = (await state.get_data())['user_id']
    await repo.add_role_to_user(user_id, Roles.ADMIN)

    text = 'Успешно!'
    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo, callback.from_user.id)
    )
    await state.clear()


@router.callback_query(
    F.data.startswith(CallbackData.CHECK_ADMIN_),
    IsSuperAdmin(),
)
async def admin_check_handler(callback: types.CallbackQuery) -> None:
    """
    Обработчик кнопки с юзернеймом админа в списке админов.
    """
    user_id, page = map(
        int,
        callback.data.replace(
            CallbackData.CHECK_ADMIN_, ''
        ).split('_')
    )

    username = await username_by_user_id(callback.bot, user_id)
    text = "Телеграм - " \
           f"{name_link(username, user_id)}"
    keyboard = check_admin_keyboard(user_id, page, sure=False)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(
    F.data.startswith(CallbackData.REMOVE_ADMIN_),
    IsSuperAdmin(),
)
async def admin_remove_handler(
        callback: types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик кнопкок "Снять роль админа" и "Точно снять роль"
    при удалении админа.
    """
    if callback.data.startswith(CallbackData.REMOVE_ADMIN_SURE_):
        user_id, page = map(
            int, callback.data.replace(
                CallbackData.REMOVE_ADMIN_SURE_, ''
            ).split('_')
        )
        await repo.remove_role_from_user(user_id, Roles.ADMIN)
        await admins_list_handler(
            callback,
            callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page}'
        )
        return

    user_id, page = map(
        int, callback.data.replace(
            CallbackData.REMOVE_ADMIN_, ''
        ).split('_')
    )

    username = await username_by_user_id(callback.bot, user_id)
    text = f"Вы точно хотите удалить из админов " \
           f"{name_link(username, user_id)}?"
    keyboard = check_admin_keyboard(user_id, page, sure=True)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
