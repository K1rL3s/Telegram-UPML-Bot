from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from bot.callbacks import AdminListData, AdminManageData, StateData
from bot.funcs.admin.admin_manage import (
    admin_add_confirm_func,
    admin_add_username_func,
    admin_check_func,
    admin_remove_func,
    admins_list_func,
)
from bot.keyboards import (
    admin_panel_keyboard,
    cancel_state_keyboard,
)
from bot.utils.enums import Actions
from bot.utils.states import AddingNewAdmin

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(AdminListData.filter())
async def admins_list_handler(
    callback: "CallbackQuery",
    callback_data: "AdminListData",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Список админов"."""
    text, keyboard = await admins_list_func(
        callback_data.page,
        repo.user,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(AdminManageData.filter(F.action == Actions.ADD))
async def admin_add_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
) -> None:
    """Обработчик кнопки "Добавить админа"."""
    await state.set_state(AddingNewAdmin.username)

    text = "Введите имя пользователя, которого хотите сделать админом."
    await callback.message.edit_text(text=text, reply_markup=cancel_state_keyboard)


@router.message(StateFilter(AddingNewAdmin.username))
async def admin_add_username_handler(
    message: "Message",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик сообщения с юзернеймом админа, которого хотят добавить."""
    text, keyboard = await admin_add_username_func(message.text, state, repo.user)
    await message.reply(text=text, reply_markup=keyboard)


@router.callback_query(
    StateData.filter(F.action == Actions.CONFIRM),
    StateFilter(AddingNewAdmin.confirm),
)
async def admin_add_confirm_handler(
    callback: "CallbackQuery",
    state: "FSMContext",
    repo: "Repository",
) -> None:
    """Обработчик кнопки "Подтвердить" при добавлении админа."""
    text = await admin_add_confirm_func(state, repo)
    await callback.message.edit_text(
        text=text,
        reply_markup=await admin_panel_keyboard(repo.user, callback.from_user.id),
    )


@router.callback_query(AdminManageData.filter(F.action == Actions.CHECK))
async def admin_check_handler(
    callback: "CallbackQuery",
    callback_data: "AdminManageData",
) -> None:
    """Обработчик кнопки с юзернеймом админа в списке админов."""
    text, keyboard = await admin_check_func(
        callback_data.user_id,
        callback_data.page,
        callback.bot,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(AdminManageData.filter(F.action == Actions.REMOVE))
async def admin_remove_handler(
    callback: "CallbackQuery",
    callback_data: "AdminManageData",
    repo: "Repository",
) -> None:
    """Обработчик кнопкок "Снять роль админа" и "Точно снять роль"."""
    text, keyboard = await admin_remove_func(
        callback_data.user_id,
        callback_data.is_sure,
        callback_data.page,
        callback.bot,
        repo,
    )
    await callback.message.edit_text(text=text, reply_markup=keyboard)
