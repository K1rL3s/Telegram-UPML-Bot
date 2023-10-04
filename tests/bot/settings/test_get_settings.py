import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from bot.settings import get_settings


@pytest.fixture(scope="function")
def env_temp_test_vars() -> "Iterator[Path, dict[str, Any]]":
    """Создание и удаление временного .env файла."""
    env_temp_test_vars = {
        "BOT_TOKEN": "test",
        "TESSERACT_PATH": "test",
        "TIMEZONE_OFFSET": "0",
        "TIMEOUT": "5",
        "POSTGRES_HOST": "127.0.0.1",
        "POSTGRES_HOST_PORT": "1234",
        "POSTGRES_OUTSIDE_PORT": "1234",
        "POSTGRES_DB": "test",
        "POSTGRES_USER": "test",
        "POSTGRES_PASSWORD": "test",
        "REDIS_HOST": "127.0.0.1",
        "REDIS_HOST_PORT": "1234",
        "REDIS_OUTSIDE_PORT": "1234",
        "REDIS_PASSWORD": "test",
    }
    env_temp_test_path = Path().cwd() / "tests" / ".env.temp"

    with open(env_temp_test_path, "w", encoding="utf-8") as f:
        f.writelines([f"{k}={v}\n" for k, v in env_temp_test_vars.items()])

    yield env_temp_test_path, env_temp_test_vars

    os.remove(env_temp_test_path)


def test_get_settings(env_temp_test_vars: "tuple[Path, dict[str, Any]]") -> None:
    """Проверка, что все данные из переданного env файла передаются в модели."""
    env_temp_test_path, env_temp_test_vars = env_temp_test_vars

    settings = get_settings(env_temp_test_path)

    assert settings.bot.token == env_temp_test_vars["BOT_TOKEN"]
    assert settings.other.tesseract_path == env_temp_test_vars["TESSERACT_PATH"]
    assert settings.other.timezone_offset == int(env_temp_test_vars["TIMEZONE_OFFSET"])
    assert settings.other.timeout == int(env_temp_test_vars["TIMEOUT"])

    assert settings.db.host == env_temp_test_vars["POSTGRES_HOST"]
    assert settings.db.host_port == int(env_temp_test_vars["POSTGRES_HOST_PORT"])
    assert settings.db.db == env_temp_test_vars["POSTGRES_DB"]
    assert settings.db.user == env_temp_test_vars["POSTGRES_USER"]
    assert settings.db.password == env_temp_test_vars["POSTGRES_PASSWORD"]

    assert settings.redis.host == env_temp_test_vars["REDIS_HOST"]
    assert settings.redis.host_port == int(env_temp_test_vars["REDIS_HOST_PORT"])
    assert settings.redis.password == env_temp_test_vars["REDIS_PASSWORD"]
