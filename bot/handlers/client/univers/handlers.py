from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.callbacks import OpenMenu, Paginator, UniverData, UniversPaginator
from bot.handlers.client.univers.funcs import univers_open_title_func
from bot.keyboards import (
    one_univer_keyboard,
    univers_cities_keyboard,
    univers_titles_keyboard,
)
from shared.database.repository.repository import Repository
from shared.utils.enums import BotMenu, PageMenu, SlashCommand, TextCommand

router = Router(name=__name__)

UNIVERS_SUBJECTS_TEXT = "Привет! Я - ВУЗы Города"
UNIVERS_TITLES_TEXT = "Привет! Я - ВУЗы {}".format


@router.callback_query(OpenMenu.filter(F.menu == BotMenu.UNIVERS))
async def univers_callback_handler(
    callback: CallbackQuery,
    repo: Repository,
) -> None:
    keyboard = await univers_cities_keyboard(page=0, univer_repo=repo.univers)
    await callback.message.edit_text(text=UNIVERS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.message(F.text == TextCommand.UNIVERS)
@router.message(Command(SlashCommand.UNIVERS))
async def univers_message_handler(
    message: Message,
    repo: Repository,
) -> None:
    keyboard = await univers_cities_keyboard(page=0, univer_repo=repo.univers)
    await message.answer(text=UNIVERS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.callback_query(Paginator.filter(F.menu == BotMenu.UNIVERS))
async def univers_cities_paginate_handler(
    callback: CallbackQuery,
    callback_data: Paginator,
    repo: Repository,
) -> None:
    keyboard = await univers_cities_keyboard(
        page=callback_data.page,
        univer_repo=repo.univers,
    )
    await callback.message.edit_text(text=UNIVERS_SUBJECTS_TEXT, reply_markup=keyboard)


@router.callback_query(
    UniverData.filter(F.city),
    UniverData.filter(F.id.is_(None)),
)
async def univers_titles_start_handler(
    callback: CallbackQuery,
    callback_data: UniverData,
    repo: Repository,
) -> None:
    keyboard = await univers_titles_keyboard(
        page=0,
        city=callback_data.city,
        univer_repo=repo.univers,
    )
    await callback.message.edit_text(
        text=UNIVERS_TITLES_TEXT(callback_data.city),
        reply_markup=keyboard,
    )


@router.callback_query(UniversPaginator.filter(F.menu == PageMenu.UNIVERS_LIST))
async def univers_titles_paginator_handler(
    callback: CallbackQuery,
    callback_data: UniversPaginator,
    repo: Repository,
) -> None:
    keyboard = await univers_titles_keyboard(
        page=callback_data.page,
        city=callback_data.city,
        univer_repo=repo.univers,
    )
    await callback.message.edit_text(
        text=UNIVERS_TITLES_TEXT(callback_data.city),
        reply_markup=keyboard,
    )


@router.callback_query(
    UniverData.filter(F.city),
    UniverData.filter(F.id.is_not(None)),
)
async def univers_open_title_handler(
    callback: CallbackQuery,
    callback_data: UniverData,
    repo: Repository,
) -> None:
    keyboard = one_univer_keyboard(
        city=callback_data.city,
        page=callback_data.page,
    )
    text = await univers_open_title_func(callback_data.id, repo.univers)
    await callback.message.edit_text(text=text, reply_markup=keyboard)
