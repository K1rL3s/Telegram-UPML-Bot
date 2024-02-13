from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.callbacks import OpenMenu, Paginator
from bot.keyboards.client.olymps import olymps_subjects_keyboard
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu

router = Router(name=__name__)

OLYMPS_SUBJECTS_TEXT = "Привет! Я - Олимпиады Предметы"


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.OLYMPS))
async def olypms_default_handler(
    callback: CallbackQuery,
    repo: Repository,
) -> None:
    keyboard = await olymps_subjects_keyboard(page=0, olymp_repo=repo.olympiads)
    await callback.message.edit_text(text=OLYMPS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.callback_query(Paginator.filter(F.menu == BotMenu.OLYMPS))
async def olymps_paginate_handler(
    callback: CallbackQuery,
    callback_data: Paginator,
    repo: Repository,
) -> None:
    keyboard = await olymps_subjects_keyboard(
        page=callback_data.page,
        olymp_repo=repo.olympiads,
    )
    await callback.message.edit_text(text=OLYMPS_SUBJECTS_TEXT, reply_markup=keyboard)
