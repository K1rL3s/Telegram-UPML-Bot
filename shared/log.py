from pathlib import Path

from loguru import logger


def configure_logs() -> None:
    """Задаёт формат логов и указывает путь записи."""
    logger.add(
        Path().cwd().absolute() / "logs" / "logs.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
        rotation="1 week",
        compression="zip",
        enqueue=True,
    )
