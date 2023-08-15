# Телеграм-бот для Югорского физико-математичкого лицея-интерната
#### Индвидуальный проект [Лесового Кирилла](https://hello.k1rles.ru)

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
    TIMEZONE=<int>
    
    POSTGRES_HOST=<ip>
    POSTGRES_PORT=<int>
    POSTGRES_DB=<str>
    POSTGRES_USER=<str>
    POSTGRES_PASSWORD=<str>
    ```

<br>

- ### Docker:

1. Иметь установленный [Docker Engine](https://docs.docker.com/engine/)

2. Собрать и запустить:

    ```
    docker compose up -d --build
    ```

3. После запуска сделать миграцию базы данных:

    ```
    docker compose exec upml-bot alembic upgrade head
    ```
