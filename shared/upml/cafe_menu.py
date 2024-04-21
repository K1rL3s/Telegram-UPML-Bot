import asyncio
import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING, Optional

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from pypdf import PdfReader

from shared.utils.datehelp import format_date, get_this_week_monday
from shared.utils.translate import CAFE_MENU_TRANSLATE

if TYPE_CHECKING:
    from shared.database.repository import MenuRepository


async def process_cafe_menu(repo: "MenuRepository", timeout: int) -> str:
    """
    Поиск, составление и сохранение расписания еды в столовой.

    :param repo: Репозиторий расписаний столовой.
    :param timeout: Таймаут для запроса на сайт лицея.
    :return: Сохранилось/Обновилось ли меню, текст результата.
    """
    if (pdf_reader := await __get_pdf_menu(timeout)) is None:
        logger.warning(text := "Не удалось найти PDF с меню")
        return text

    if (menu_date := __compare_pdf_date(pdf_reader)) is None:
        logger.warning(text := "Не удалось сравнять дату PDF и текущей недели")
        return text

    await __parse_pdf_menu(repo, pdf_reader, menu_date)

    logger.info(text := "Расписание еды обновлено!")
    return text


async def __get_pdf_menu(timeout: int = 5) -> "Optional[PdfReader]":
    """
    Ищет и возвращает файл с недельным расписанием питания с сайта лицея.

    :return: PdfReader если файл существует, иначе None
    """
    pdf_url = (
        "https://yufmli.gosuslugi.ru/netcat_files/47/515/"
        "Menyu_{day:0>2}_{month:0>2}_{year}_krugl.pdf"
    )

    menu_date = get_this_week_monday() - dt.timedelta(days=1)
    # Поиск с воскресенья по воскресенье
    # Число и месяц изменяются сами, поэтому ссылка будет корректной
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        days_at_week = 7
        for _ in range(days_at_week):
            async with session.get(
                pdf_url.format(
                    day=menu_date.day,
                    month=menu_date.month,
                    year=menu_date.year,
                ),
            ) as response:
                if response.headers.get("content-type") == "application/pdf":
                    return PdfReader(BytesIO(await response.read()))

            menu_date += dt.timedelta(days=1)
            await asyncio.sleep(0.25)  # На случай, чтобы госуслуги не легли от нагрузки

    return None


def __compare_pdf_date(pdf_reader: "PdfReader") -> "Optional[dt.date]":
    """
    Возвращает дату, с которой начинается расписание еды в пдф файле.

    :param pdf_reader: PDF файл.
    :return: Дата начала расписания еды или None, если не удалось сравнять дату.
    """
    pages = __linearize_pdf_pages(pdf_reader)

    for i, page in enumerate(pages):
        check_date = get_this_week_monday()
        for _ in range(len(pages)):
            if format_date(check_date) in page:
                return check_date - dt.timedelta(days=i)
            check_date += dt.timedelta(days=1)
    return None


def __linearize_pdf_pages(pdf_reader: "PdfReader") -> list[str]:
    return [" ".join(page.extract_text().split()) for page in pdf_reader.pages]


async def __parse_pdf_menu(
    repo: "MenuRepository",
    pdf_reader: "PdfReader",
    date: "dt.date",
) -> None:
    """
    Идёт по PDF недельного расписания меню и добавляет меню каждого дня в бд.

    :param repo: Репозиторий расписаний столовой.
    :param pdf_reader: PDF файл.
    :param date: Дата, с которой начинается расписание в файле.
    """
    for page in pdf_reader.pages:
        text_menu = " ".join(page.extract_text().split())
        meals = __parse_page_to_meals(text_menu)
        meals_to_info = dict(zip(CAFE_MENU_TRANSLATE.keys(), meals))
        await repo.save_or_update_to_db(date, **meals_to_info)

        date += dt.timedelta(days=1)


def __parse_page_to_meals(text_menu: str) -> list[str]:
    """
    Разбение текста страницы расписания еды на приёмы пищи.

    :param text_menu: Текст страницы.
    :return: Расписание еды по распорядку дня.
    """
    food_times = [
        ("автрак", "автрак"),
        ("автрак", "обед"),
        ("обед", "полдник"),
        ("полдник", "ужин"),
        ("ужин", "итого"),
    ]

    meals = []
    for start_sub, end_sub in food_times:
        meal, _, end_index = __get_meal(text_menu, start_sub, end_sub)
        meals.append(__normalize_meal(meal) if meal else None)
        if end_index is not None:
            text_menu = text_menu[end_index:]

    return meals


def __get_meal(
    menu: str,
    start_sub: str,
    end_sub: str,
) -> tuple[Optional[str], Optional[int], Optional[int]]:
    """
    Возвращает строку с едой для конкретного приёма пищи.

    Подстроки start_sub и end_sub разделяют начало и конец нужной строки.

    :param menu: Меню столовой на день без переносов строки.
    :param start_sub: Начальное ключевое слово.
    :param end_sub: Конечное ключевое слово.
    :return: Строка формата "{блюдо} {числа} {блюдо} {числа} ...",
             начальный и конечный индексы по строке меню.
    """
    try:
        start_index = menu.lower().index(start_sub) + len(start_sub)
    except ValueError:
        start_index = None

    try:
        end_index = menu.lower().rindex(end_sub)
    except ValueError:
        end_index = None

    if start_index is None or end_index is None:
        return None, start_index, end_index

    return menu[start_index:end_index].strip(), start_index, end_index


# Это самое жуткое, что я когда-либо писал, и оно работает :(
def __normalize_meal(one_meal: str) -> str:
    """
    Принимает строку из ``def __get_meal`` и переделывает её в читаемый вид.

    (Каждое блюдо с новой строки без лишних символов).

    :param one_meal: Строка с конкретным приёмом пищи (завтрак, обед).
    :return: Читаемый вид этой строки
    """
    meal = " ".join(one_meal.replace(",", "").strip().split())

    dishes = []
    dish = ""
    for i, char in enumerate(meal):
        if char.isdigit():
            if len(set(dish)) > 2:
                dish = dish.strip("[].I/, \t\n")
                if dish.startswith("Д "):
                    dish = dish[2:]
                dishes.append(dish)
                dish = ""
        elif char == " ":
            if not meal[i - 1].isdigit():
                dish += char
        else:
            dish += char

    return "\n".join(dishes)
