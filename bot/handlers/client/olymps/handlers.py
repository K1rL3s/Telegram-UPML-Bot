from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OlympData, OlympsPaginator, OpenMenu, Paginator
from bot.keyboards import (
    olymps_subjects_keyboard,
    olymps_titles_keyboard,
    one_olymp_keyboard,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu, PageMenu, SlashCommand, TextCommand

from .funcs import olymps_open_title_func

router = Router(name=__name__)

OLYMPS_SUBJECTS_TEXT = "Привет! Я - Олимпиады Предметы"
OLYMPS_TITLES_TEXT = "Привет! Я - Олимпиады {}".format


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.OLYMPS))
async def olymps_callback_handler(
    callback: CallbackQuery,
    repo: Repository,
) -> None:
    keyboard = await olymps_subjects_keyboard(page=0, olymp_repo=repo.olympiads)
    await callback.message.edit_text(text=OLYMPS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommand.OLYMPS)
@router.message(Command(SlashCommand.OLYMPS))
async def olymps_message_handler(
    message: Message,
    repo: Repository,
) -> None:
    keyboard = await olymps_subjects_keyboard(page=0, olymp_repo=repo.olympiads)
    await message.answer(text=OLYMPS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.callback_query(Paginator.filter(F.menu == BotMenu.OLYMPS))
async def olymps_subjects_paginate_handler(
    callback: CallbackQuery,
    callback_data: Paginator,
    repo: Repository,
) -> None:
    keyboard = await olymps_subjects_keyboard(
        page=callback_data.page,
        olymp_repo=repo.olympiads,
    )
    await callback.message.edit_text(text=OLYMPS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.callback_query(
    OlympData.filter(F.subject),
    OlympData.filter(F.id.is_(None)),
)
async def olymps_titles_start_handler(
    callback: CallbackQuery,
    callback_data: OlympData,
    repo: Repository,
) -> None:
    keyboard = await olymps_titles_keyboard(
        page=0,
        subject=callback_data.subject,
        olymp_repo=repo.olympiads,
    )
    await callback.message.edit_text(
        text=OLYMPS_TITLES_TEXT(callback_data.subject),
        reply_markup=keyboard,
    )


@router.callback_query(OlympsPaginator.filter(F.menu == PageMenu.OLYMPS_LIST))
async def olymps_titles_paginator_handler(
    callback: CallbackQuery,
    callback_data: OlympsPaginator,
    repo: Repository,
) -> None:
    keyboard = await olymps_titles_keyboard(
        page=callback_data.page,
        subject=callback_data.subject,
        olymp_repo=repo.olympiads,
    )
    await callback.message.edit_text(
        text=OLYMPS_TITLES_TEXT(callback_data.subject),
        reply_markup=keyboard,
    )


@router.callback_query(OlympData.filter(F.subject), OlympData.filter(F.id.is_not(None)))
async def olymps_open_title_handler(
    callback: CallbackQuery,
    callback_data: OlympData,
    repo: Repository,
) -> None:
    keyboard = one_olymp_keyboard(
        subject=callback_data.subject,
        page=callback_data.page,
    )
    text = await olymps_open_title_func(callback_data.id, repo.olympiads)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
