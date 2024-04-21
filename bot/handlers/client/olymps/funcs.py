from shared.database.models import Olymp
from shared.database.repository import OlympRepository


async def olymps_open_title_func(olymp_id, repo: OlympRepository) -> str:
    olymp = await repo.get_by_id(olymp_id)
    return _format_olympiad(olymp)


def _format_olympiad(olymp: Olymp) -> str:
    return f"<b>{olymp.title}, {olymp.subject}</b>\n\n{olymp.description}"
