import asyncio
import datetime as dt
from pathlib import Path
from typing import TYPE_CHECKING

from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import cell
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.database import database_init
from bot.database.repository.repository import Repository
from bot.settings import get_settings
from bot.utils.datehelp import date_today, datetime_now


if TYPE_CHECKING:
    from bot.database.repository import EducatorsScheduleRepository


async def load_educators_from_xlsx(repo: "EducatorsScheduleRepository") -> None:

    today = date_today()
    current_date = dt.date(year=today.year, month=today.month, day=1)
    while current_date.month == today.month:
        educators_names = parse_excel(current_date.day)
        schedule = format_text(educators_names)

        await repo.save_or_update_to_db(
            date=current_date,
            schedule_text=schedule,
        )

        current_date += dt.timedelta(days=1)


def parse_excel(day: int) -> list[str]:
    wb: Workbook = load_workbook(Path().cwd() / "resources" / "educators.xlsx")
    ws: Worksheet = wb.active

    list_educators: list[str] = []
    index_educarors: int = 3
    work_cell: cell = ws.cell(index_educarors, day + 2)

    while not work_cell.value is None:
        if "В" not in work_cell.value:
            list_educators.append(work_cell.value + " " + ws.cell(index_educarors, 1).value)
        index_educarors += 1
        work_cell = ws.cell(index_educarors, day + 2)

    list_educators.sort(key=educators2time)
    today = date_today()
    day = dt.date(year=today.year, month=today.month, day=day).replace(1).day
    index_educarors = 3
    work_cell: cell = ws.cell(index_educarors, day + 2)

    while not work_cell.value is None:
        if "В" not in work_cell.value:
            if work_cell.value.split("-")[1][0] == "9":
                (list_educators.insert(0, work_cell.value + " " + ws.cell(index_educarors, 1).value))
        index_educarors += 1
        work_cell = ws.cell(index_educarors, day + 2)

    list_educators = map(format_educators_line, list_educators)
    return list_educators
def format_educators_line(line: str) -> str:
    list_line = line.split()
    line = list_line[0].split("-")[0] + ":00-" + list_line[0].split("-")[1] + ":00 "
    line += list_line[1] + " " + list_line[2] + " " + list_line[3]
    return line
def educators2time(educators: str) -> int:
    time = educators.split("-")[0]
    return int(time)
def format_text(educators_names: list[str]) -> str:
    return '\n'.join(educators_names)


async def main() -> None:
    settings = get_settings()
    session_maker: "async_sessionmaker[AsyncSession]" = await database_init(settings.db)

    async with session_maker.begin() as session:
        repo = Repository(session)
        educators_repo = repo.educators
        await load_educators_from_xlsx(educators_repo)


if __name__ == "__main__":
    asyncio.run(main())
