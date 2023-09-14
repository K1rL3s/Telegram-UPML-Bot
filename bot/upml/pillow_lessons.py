import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

from PIL import Image
import pytesseract

from bot.utils.datehelp import date_today

if TYPE_CHECKING:
    from PIL.PyAccess import PyAccess


GRADE_CHARS = "01"


def parse_one_lessons_file(
    image: "BytesIO",
    tesseract_path: str,
) -> tuple[str, "dt.date", list["BytesIO"]]:
    """
    Основная функция в файле, выполняет всю работу, вызывая другие функции.

    :param image: Исходник расписания.
    :param tesseract_path: Путь до exeшника тессеракта.
    :return: Дата, класс, полное расписание, расписания по классам.
    """
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    lessons = Image.open(image)

    first_line_y = _y_first_horizontal_line(lessons)
    prefix_end_x = _x_prefix_for_lessons(lessons, first_line_y + 2)

    prefix_image = _crop_prefix(lessons, prefix_end_x)
    date_image, preffix_up_y, prefix_down_y = _crop_date(
        lessons,
        prefix_end_x,
        first_line_y,
    )
    lessons_date = _tesseract_date(date_image)
    classes = _combine_prefix_classes_date(
        _crop_lessons_by_class(lessons, prefix_end_x, first_line_y),
        prefix_image,
        date_image,
        preffix_up_y,
        prefix_down_y,
    )

    grade_image = _crop_grade(lessons, prefix_end_x, first_line_y)
    grade = _tesseract_grade(grade_image)

    bytesio_classes: list[BytesIO] = []
    for class_image in classes:
        class_image.save(buffer := BytesIO(), format="PNG")
        bytesio_classes.append(buffer)

    return grade, lessons_date, bytesio_classes


def _is_pixel_black(pixel: tuple[int, int, int]) -> bool:
    """Чёрный ли пиксель. Граница подобрана опытным путём."""
    return all(color <= 80 for color in pixel)


def _is_pixel_white(pixel: tuple[int, int, int]) -> bool:
    """Белый ли пиксель. Граница подобрана опытным путём."""
    return all(color >= 200 for color in pixel)


def _y_first_horizontal_line(image: "Image.Image") -> int:
    """
    Поиск первой горизонтальной чёрной полосы.

    :param image: Исходник расписания уроков.
    :return: Высота первой чёрной полосы.
    """
    width, height = image.size
    pixels: PyAccess | None = image.load()

    x, y = width // 2, 0
    while y < height and not _is_pixel_black(pixels[x, y]):
        y += 1

    if y == height:
        raise ValueError("Не удалось найти первую горизонтальную линию")

    return y


def _x_prefix_for_lessons(image: "Image.Image", y: int) -> int:
    """
    Поиск конца "префиксной части" расписания (та, которая "Пара Урок Время" слева).

    :param image: Исходник расписания уроков.
    :param y: На какой высоте считать черные вертикальные линии.
    :return: Четвёртая вертикальная линия.
    """
    width, x = image.width, 0
    pixels: PyAccess | None = image.load()

    black_count = 0

    while black_count < 4 and x < width -1:
        x += 1
        if (
            x > 0
            and _is_pixel_white(pixels[x, y])
            and _is_pixel_black(pixels[x - 1, y])
        ):
            black_count += 1

    if x == width or black_count < 4:
        raise ValueError("Не найдена граница префикса расписания")

    return x - 1


def _crop_prefix(image: "Image.Image", x: int) -> "Image.Image":
    """
    Вырезка "префиксной части" слева (та, которая "Пара Урок Время").

    :param image: Исходник расписания.
    :param x: X конца префиксной части расписания.
    :return: Префиксная часть.
    """
    return image.crop((0, 0, x + 1, image.height))


def _crop_date(image: "Image.Image", x: int, y: int) -> tuple["Image.Image", int, int]:
    """
    Вырезка дня недели и даты с серой полосы.

    :param image: Исходник расписания.
    :param x: X четвёртой вертикальной линии.
    :param y: Y первой горизонтальной линии.
    :return: Максимально обрезанная часть с днём недели с датой расписания,
             верхняя и нижняя границы серой полосы относительно
             исходника расписания.
    """
    width, height = image.size
    pixels: PyAccess | None = image.load()

    # Получаю верх и низ серой полосы
    while y < height and _is_pixel_black(pixels[x, y]):
        y += 1

    up_y = y

    while y < height and not _is_pixel_black(pixels[x, y]):
        y += 1

    down_y = y - 1

    left_x, right_x = None, None

    start_x = width // 3
    while left_x is None and start_x < width // 3 * 2 + 1:
        for height_y in range(up_y, down_y + 1):
            if _is_pixel_black(pixels[start_x, height_y]):
                left_x = start_x
                break
        start_x += 1

    end_x = width // 3 * 2
    while right_x is None and end_x > left_x - 1:
        for height_y in range(up_y, down_y + 1):
            if _is_pixel_black(pixels[end_x, height_y]):
                right_x = end_x
                break
        end_x -= 1

    if (
        left_x is None
        or right_x is None
        or abs(left_x - right_x) <= 1
        or abs(right_x - down_y) <= 1
        or abs(up_y - down_y) <= 1
    ):
        raise ValueError("Не удалось получить дату с расписания")

    return image.crop((left_x, up_y, right_x + 2, down_y + 1)), up_y, down_y


def _tesseract_date(image: "Image.Image") -> dt.date:
    """
    Преобразование изображение из ``def _crop_date`` в объект даты.

    :param image: Картинка с текстом.
    :return: Дата.
    """
    dd_mm = (
        pytesseract.image_to_string(
            image,
            lang="rus",
            config="--psm 10 --oem 3",
        )
        .lower()
        .replace("$", "8")  # Костыль, восьмёрку распознаёт как доллар :(
        .split()
    )[-1]

    day, month = map(int, dd_mm.split("."))

    return dt.date(day=day, month=month, year=date_today().year)


def _crop_lessons_by_class(image: "Image.Image", x: int, y: int) -> list["Image.Image"]:
    """
    Вырезает из расписания каждый класс.

    :param image: Исходник расписания.
    :param x: X конца префиксной части расписания.
    :param y: Y первой горизонтальной линии.
    :return: Список с тремя картинками.
    """
    y += 1
    x += 1

    image = image.crop((x, 0, image.width, image.height))
    width, height = image.size
    pixels: PyAccess | None = image.load()

    images = []

    for _ in range(3):
        while x < width and not _is_pixel_black(pixels[x, y]):
            x += 1

        if x == width:
            raise ValueError("Не удалось найти конец уроков класса")

        cropped = image.crop((1, 0, x + 1, height))
        images.append(cropped)

        image = image.crop((x, 0, width, height))
        width, height = image.size
        pixels: PyAccess | None = image.load()
        x = 1

    return images


def _combine_prefix_classes_date(
    classes: list["Image.Image"],
    prefix: "Image.Image",
    date_im: "Image.Image",
    up_y: int,
    down_y: int,
) -> list["Image.Image"]:
    """
    Комбинация префикса расписания с урокам каждого класса и датой расписания.

    :param classes: Уроки каждого класса отдельно.
    :param prefix: Префиксная часть.
    :param date_im: День недели и дата.
    :param up_y: Верхняя граница серой полосы.
    :param down_y: Нижняя граница серой полосы.
    :return: Уроки каждого класса с префиксом слева.
    """
    new_classes = []

    for image in classes:
        new_image = Image.new("RGB", (image.width + prefix.width, image.height))
        new_image.paste(prefix, (0, 0))
        new_image.paste(image, (prefix.width, 0))

        date_x = (new_image.width - date_im.width) // 2
        color = new_image.getpixel((date_x, up_y))
        new_image.paste(
            Image.new("RGB", (new_image.width // 2, down_y - up_y), color),
            (new_image.width // 4, up_y),
        )
        new_image.paste(date_im, ((new_image.width - date_im.width) // 2, up_y))
        new_classes.append(new_image)

    if len(classes) != 3:  # Три класса на одном расписании
        raise ValueError("Не удалось разделить расписание по классам.")

    return new_classes


def _crop_grade(image: "Image.Image", x: int, y: int) -> "Image.Image":
    """
    Ищет, расписание для 10 или 11 классов.

    :param image: Исходник расписания.
    :param x: X конца префиксной части расписания.
    :param y: Y первой горизонтальной линии.
    :return: Вырезанная строка с классом.
    """
    x += 1
    y += 1
    width, height = image.size
    left_x, up_y = x, y
    pixels: PyAccess | None = image.load()

    while x < width and not _is_pixel_black(pixels[x, y]):
        x += 1

    if x == width:
        raise ValueError("Не удалось найти чёрную полосу после префикса")

    x -= 2

    while y < height and not _is_pixel_black(pixels[x, y]):
        y += 1

    if left_x == x or up_y == y:
        raise ValueError("Не удалось правильно выделить класс")

    return image.crop((left_x, up_y, x, y))


def _tesseract_grade(image: "Image.Image") -> str:
    """
    Преобразование изображение из ``def _crop_grade`` в строку с классом.

    :param image: Картинка с текстом.
    :return: Класс.
    """
    text = pytesseract.image_to_string(
        image,
        config=f"--psm 10 --oem 3 -c tessedit_char_whitelist={GRADE_CHARS}",
    )
    if "10" in text:
        return "10"
    if "11" in text:
        return "11"

    raise ValueError("Не удалось определить класс")
