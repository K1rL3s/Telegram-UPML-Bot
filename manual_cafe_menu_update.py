import asyncio

from src.database.db_session import global_init
from src.upml.save_cafe_menu import save_cafe_menu
from src.utils.consts import Config


async def main():
    global_init(Config.DATABASE_PATH)
    result = await save_cafe_menu()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
