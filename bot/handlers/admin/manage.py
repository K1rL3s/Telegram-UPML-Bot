from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.callbacks import AdminCheck, AdminEditRole, AdminList, InStateData
from bot.filters import IsSuperAdmin
from bot.funcs.admin.admin_manage import (
    admin_check_func,
    admins_list_func,
    edit_role_action_func,
    edit_role_choose_role_func,
    edit_role_confirm_func,
    edit_role_username_func,
)
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
)
from bot.utils.enums import Actions
from bot.utils.funcs import username_by_user_id
from bot.utils.states import EditingRoles

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)
router.message.filter(IsSuperAdmin())
router.callback_query.filter(IsSuperAdmin())


@router.callback_query(AdminList.filter())
async def admins_list_handler(
    callback: "CallbackQuery",
    callback_data: "AdminList",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Список админов"."""
    text, keyboard = await admins_list_func(
        callback_data.page,
        repo.user,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(AdminCheck.filter())
async def admin_check_roles_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    repo: "Repository",
) -> None:
    """Обработчик кнопки с юзернеймом админа в списке админов."""
    text, keyboard = await admin_check_func(
        callback_data.user_id,
        callback_data.page,
        callback.bot,
        repo.user,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    AdminEditRole.filter(F.action == Actions.REMOVE),
    AdminEditRole.filter(F.user_id.is_not(None)),
)
async def role_remove_directly_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок снятия ролей ролей при просмотре админа."""
    username = await username_by_user_id(callback.bot, callback_data.user_id)

    await state.set_state(EditingRoles.confirm)
    await state.update_data(
        action=callback_data.action,
        user_id=callback_data.user_id,
        username=username,
    )
    text, keyboard = await edit_role_choose_role_func(callback_data.role, state)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    AdminEditRole.filter(F.action == Actions.EDIT),
    AdminEditRole.filter(F.role.is_(None)),
    AdminEditRole.filter(F.user_id.is_(None)),
)
async def edit_role_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Изменить роли"."""
    await state.set_state(EditingRoles.username)

    text = "Введите имя пользователя, у которого хотите изменить роли."
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingRoles.username))
async def edit_role_username_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик сообщения с юзернеймом, которому хотят изменить роли."""
    text, keyboard = await edit_role_username_func(message.text, state, repo.user)
    await message.reply(text=text, reply_markup=keyboard)


@router.callback_query(StateFilter(EditingRoles.action), AdminEditRole.filter())
async def edit_role_action_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопок действия с ролями (добавить или удалить)."""
    text, keyboard = await edit_role_action_func(
        callback_data.action,
        state,
        repo.user,
        repo.role,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    StateFilter(EditingRoles.role),
    AdminEditRole.filter(F.role.is_not(None)),
)
async def edit_role_choose_role_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок с ролями при редактировании ролей пользователя."""
    text, keyboard = await edit_role_choose_role_func(callback_data.role, state)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    InStateData.filter(F.action == Actions.CONFIRM),
    StateFilter(EditingRoles.confirm),
)
async def edit_role_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Подтвердить" при добавлении админа."""
    text = await edit_role_confirm_func(state, repo)
    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )
