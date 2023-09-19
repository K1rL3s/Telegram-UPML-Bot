FROM python:3.11.5-slim-bullseye as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && \
    pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r ./requirements.txt


FROM python:3.11.5-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TESSERACT_PATH="/usr/bin/tesseract"

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Апдейт здесь из-за установки тессеракта :(
RUN apt-get update && \
    apt-get install -y tesseract-ocr-rus && \
    pip install --no-cache --no-cache-dir /wheels/*

COPY ./bot ./bot
COPY ./migration ./migration
COPY ./alembic.ini ./alembic.ini

CMD ["python", "-m", "bot"]