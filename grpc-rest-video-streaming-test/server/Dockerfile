FROM python:3.12-slim

WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# 프로젝트 파일 복사
COPY pyproject.toml poetry.lock ./
COPY proto/ ./proto/
COPY server/ ./server/
COPY generated/ ./generated/

# 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 서버 실행
CMD ["poetry", "run", "python", "server/server.py"] 