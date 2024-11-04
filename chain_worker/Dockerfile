# Python 3.12 기반 이미지 사용
FROM python:3.12-slim

# 작업 디렉터리 설정
WORKDIR /app

# Poetry 설치 및 환경 구성
RUN pip install --no-cache-dir poetry

# pyproject.toml 파일을 복사하여 종속성을 설치
COPY pyproject.toml .
COPY poetry.lock . 

# Poetry를 사용하여 종속성 설치
RUN poetry config virtualenvs.create false && poetry install --no-root

# 나머지 코드와 애플리케이션 파일 복사
COPY . .

# 기본 명령을 Celery 워커로 설정
CMD ["celery", "-A", "app.worker.celery_app", "worker", "--loglevel=info"]