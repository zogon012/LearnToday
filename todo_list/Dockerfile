FROM python:3.11-slim

WORKDIR /app

# poetry 설치
RUN pip install poetry

# pyproject.toml, poetry.lock, README.md, alembic.ini, alembic 복사
COPY pyproject.toml poetry.lock* README.md ./


# 의존성 설치 (가상환경 비활성화 옵션)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# 앱 코드 복사
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 