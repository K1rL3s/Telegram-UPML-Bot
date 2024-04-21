from shared.database.models import Univer
from shared.database.repository import UniverRepository


async def univers_open_title_func(olymp_id, repo: UniverRepository) -> str:
    univer = await repo.get_by_id(olymp_id)
    return _format_univer(univer)


def _format_univer(univer: Univer) -> str:
    return f"<b>{univer.title}, {univer.city}</b>\n\n{univer.description}"
