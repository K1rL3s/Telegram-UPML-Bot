# Телеграм-бот для Югорского физико-математического лицея-интерната
#### Индивидуальный проект [Лесового Кирилла](https://hello.k1rles.ru)

## Запуск

1. Склонировать репозиторий и перейти в него:

    ```
    git clone https://github.com/K1rL3s/Telegram-UPML-Bot.git
    cd ./Telegram-UPML-Bot
    ```

2. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`):

    ```
    BOT_TOKEN=<token>
    TESSERACT_PATH=<path>
    TIMEZONE_OFFSET=<int>
    TIMEOUT=<int>
    
    POSTGRES_HOST=<ip>
    POSTGRES_HOST_PORT=<int>
    POSTGRES_OUTSIDE_PORT=<int>
    POSTGRES_DB=<str>
    POSTGRES_USER=<str>
    POSTGRES_PASSWORD=<str>

    REDIS_HOST=<ip>
    REDIS_HOST_PORT=<int>
    REDIS_OUTSIDE_PORT=<int>
    REDIS_PASSWORD=<str>
    ```

- ### Docker:

1. Иметь установленный [Docker Engine](https://docs.docker.com/engine/)

2. Собрать и запустить:

    ```
    docker compose up -d --build
    ```

3. После запуска сделать миграцию базы данных:

    ```
    docker compose exec bot alembic upgrade head
    ```

4. Опционально, загрузить расписание воспитателей:

    ```
    docker compose exec -it bot bash
    PYTHONPATH=/app python ./shared/upml/educators_excel.py
    ```
