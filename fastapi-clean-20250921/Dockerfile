FROM python:3.12-slim AS base

ENV POETRY_VERSION=1.7.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry lock --no-interaction \
    && poetry install --no-root --no-interaction --no-ansi

COPY src ./src
COPY tests ./tests
COPY .env.example ./

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
