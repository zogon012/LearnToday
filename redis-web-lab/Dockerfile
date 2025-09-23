# Multi-stage Dockerfile for FastAPI application
FROM python:3.11-slim as requirements-stage

# Poetry 및 export 플러그인 설치
RUN pip install poetry poetry-plugin-export

# Poetry 설정
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# 작업 디렉토리 설정
WORKDIR /tmp

# Poetry 설정 파일 복사
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 의존성을 requirements.txt로 export
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 최종 이미지
FROM python:3.11-slim

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app/app

# 사용자 생성 (보안상 root 사용 금지)
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# 포트 노출
EXPOSE 8000

# 환경변수 설정
ENV PYTHONPATH=/app
ENV REDIS_URL=redis://redis:6379

# 헬스체크 설정
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
