FROM python:3.13.0a2-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r ./requirements.txt


FROM python:3.13.0a2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TESSERACT_PATH="/usr/bin/tesseract"

WORKDIR /app

COPY --from=builder /app/wheels /wheels

# Апдейт здесь из-за установки тессеракта :(
RUN apt-get update && \
    apt-get install -y tesseract-ocr-rus && \
    pip install --no-cache-dir /wheels/*

COPY ./bot ./bot
COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini

CMD ["python", "-m", "bot"]