FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

ENV POETRY_VENV_IN_PROJECT=false
ENV POETRY_CACHE_DIR=/opt/poetry_cache

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-root \
    && rm -rf $POETRY_CACHE_DIR

COPY main.py ./

CMD ["python", "main.py"]