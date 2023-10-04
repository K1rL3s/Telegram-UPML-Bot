from collections.abc import Iterator
from pathlib import Path

import pytest

from bot.settings import get_settings, Settings


@pytest.fixture(scope="session")
def settings() -> "Iterator[Settings]":
    """Фикстура, добавляющая настройки по умолчанию."""
    yield get_settings(Path().cwd() / ".env.test")
