from io import BytesIO
from datetime import date, timedelta

from loguru import logger
from pypdf import PdfReader

from bot.config import Config
from bot.database.db_funcs import Repository
from bot.utils.datehelp import format_date, get_this_week_monday


async def save_cafe_menu(repo: Repository) -> tuple[bool, str]:
    """
    Основная функция в файле, выполняет всю работу, вызывая другие функции.

    :return: Сохранилось/Обновилось ли меню.
    """

    if (pdf_reader := await _get_pdf_menu()) is None:
        logger.warning(text := 'Не удалось найти PDF с меню')
        return False, text

    menu_date = get_this_week_monday()
    add_counter = 0

    menu = ' '.join(pdf_reader.pages[0].extract_text().split())
    while add_counter < 7 and format_date(menu_date) not in menu:
        menu_date += timedelta(days=1)
        add_counter += 1

    if add_counter >= 7:
        logger.warning(text := 'Не удалось сравнять дату PDF и текущей недели')
        return False, text

    await _process_pdf_menu(repo, pdf_reader, menu_date)
    return True, 'Расписание еды обновлено!'


def _get_meal(menu: str, start_sub: str, end_sub: str) -> tuple[str, int, int]:
    """
    Возвращает строку с едой для конкретного приёма пищи,
    ограниченного ключевыми подстроками start_sub и end_sub.

    :param menu: Меню столовой на день без переносов строки.
    :param start_sub: Начальное ключевое слово.
    :param end_sub: Конечное ключевое слово.
    :return: Строка формата "{блюдо} {числа} {блюдо} {числа} ...",
             начальный и конечный индексы по строке меню.
    """

    start_index = menu.lower().index(start_sub) + len(start_sub)
    end_index = menu.lower().rindex(end_sub)
    return menu[start_index:end_index].strip(), start_index, end_index


# РАБОТАЕТ НЕ ТРОГАТЬ РАБОТАЕТ НЕ ТРОГАТЬ РАБОТАЕТ НЕ ТРОГАТЬ
def _normalize_meal(meal: str) -> str:
    """
    Принимает строку из ``def get_string_meal``
    и переделывает её в читаемый вид
    (каждое блюдо с новой строки без лишних символов).

    :param meal: Строка с конкретным приёмом пищи (завтрак, обед).
    :return: Читаемый вид этой строки
    """

    meal = ' '.join(meal.replace(',', '').strip().split())

    dishes = []
    dish = ""
    for i, ch in enumerate(meal):
        if ch.isdigit():
            if len(set(dish)) > 2:
                dish = dish.strip('[].I/, \t\n')
                if dish.startswith('Д '):
                    dish = dish[2:]
                dishes.append(dish)
                dish = ""
        elif ch == ' ':
            if not meal[i - 1].isdigit():
                dish += ch
        else:
            dish += ch

    return '\n'.join(dishes)


async def _get_pdf_menu() -> None | PdfReader:
    """
    Ищет и возвращает файл с недельным расписанием
    круглосуточного горячего питания с сайта лицея.

    :return: PdfReader если файл существует, иначе None
    """

    # Передавать число, месяц, год
    # print(pdf_url(2, 5, 2023))
    pdf_url = 'https://ugrafmsh.ru/wp-content/uploads/' \
              '{2}/{1:0>2}/menyu-{0:0>2}-{1:0>2}-{2}-krugl.pdf'.format

    menu_date = get_this_week_monday() - timedelta(days=1)

    # Ищем в воскресенье, понедельник, вторник и среду.
    # Число и месяц изменяются сами, поэтому ссылка будет корректной.
    for i in range(4):
        response = await Config.async_session.get(
            pdf_url(menu_date.day, menu_date.month, menu_date.year)
        )
        if response.headers.get('content-type') == 'application/pdf':
            return PdfReader(BytesIO(response.content))

        menu_date += timedelta(days=1)

    return None


async def _process_pdf_menu(
        repo: Repository,
        pdf_reader: PdfReader,
        menu_date: date,
) -> None:
    """
    Идёт по PDF недельного распсания и добавляет меню каждого дня в бд.

    :param pdf_reader: PDF файл.
    :param menu_date: Дата, с которой начинается расписание в файле.
    """

    for page in pdf_reader.pages:
        text_menu = ' '.join(page.extract_text().split())
        food_times = [
            ('автрак', 'автрак'),
            ('автрак', 'обед'),
            ('обед', 'полдник'),
            ('полдник', 'ужин'),
            ('ужин', 'итого'),
        ]

        meals = []
        for start_sub, end_sub in food_times:
            meal, start, end = _get_meal(text_menu, start_sub, end_sub)
            meals.append(_normalize_meal(meal))
            text_menu = text_menu[end:]

        await repo.save_or_update_menu(
            menu_date,
            *meals
        )

        menu_date += timedelta(days=1)
