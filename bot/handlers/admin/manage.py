from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.callbacks import AdminCheck, AdminEditRole, AdminList, InStateData
from bot.filters import IsSuperAdmin
from bot.funcs.admin.manage import (
    admins_list_func,
    check_admin_roles_func,
    edit_role_choose_role_func,
    edit_role_confirm_func,
    edit_role_confirm_sure_func,
    edit_role_directly_func,
    edit_role_username_func,
)
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
)
from bot.utils.enums import Actions
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
    text, keyboard = await check_admin_roles_func(
        callback_data.user_id,
        callback_data.page,
        repo.user,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(
    AdminEditRole.filter(F.role.is_not(None)),
    AdminEditRole.filter(F.user_id.is_not(None)),
)
async def edit_roles_directly_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки изменения ролей при просмотре админа."""
    text, keyboard = await edit_role_directly_func(
        callback_data.user_id,
        repo.user,
        state,
    )
    await callback.bot.edit_message_text(
        text=text,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard,
    )


@router.callback_query(
    AdminEditRole.filter(F.action == Actions.EDIT),
    AdminEditRole.filter(F.user_id.is_(None)),
)
async def edit_roles_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Изменить роли"."""
    await state.set_state(EditingRoles.username)

    text = "Введите имя пользователя, у которого хотите изменить роли."
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(EditingRoles.username))
async def edit_roles_username_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик сообщения с юзернеймом, которому хотят изменить роли."""
    text, keyboard = await edit_role_username_func(
        message.text,
        state,
        repo.user,
    )

    await message.answer(text=text, reply_markup=keyboard)
    await message.delete()


@router.callback_query(
    StateFilter(EditingRoles.roles),
    AdminEditRole.filter(F.user_id.is_(None)),
)
async def edit_roles_choose_role_handler(
    callback: "CallbackQuery",
    callback_data: "AdminEditRole",
    state: "FSMContext",
) -> None:
    """Обработчик кнопок с ролями при редактировании ролей пользователя."""
    text, keyboard = await edit_role_choose_role_func(
        callback_data.role,
        state,
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    StateFilter(EditingRoles.roles),
    InStateData.filter(F.action == Actions.CONFIRM),
)
async def edit_roles_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Подтвердить" при добавлении админа."""
    text, keyboard = await edit_role_confirm_func(state)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    StateFilter(EditingRoles.confirm),
    InStateData.filter(F.action == Actions.CONFIRM),
)
async def edit_roles_confirm_sure_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Подтвердить" при добавлении админа, точное подтверждение."""
    text = await edit_role_confirm_sure_func(state, repo.user_role)
    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )
