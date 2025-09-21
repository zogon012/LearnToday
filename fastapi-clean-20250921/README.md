# FastAPI Clean Architecture Example

FastAPI, PostgreSQL, Docker, Poetry 기반의 간단한 사용자(User) 예제 프로젝트입니다. 클린 아키텍처 스타일을 따르며, 테스트와 린팅(Ruff)까지 실행할 수 있는 구성을 담고 있습니다.

## 프로젝트 구조

```
.
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── src/app
│   ├── config.py
│   ├── main.py
│   └── user
│       ├── api/v1/routes/users.py        # 프레젠테이션 (FastAPI 라우터)
│       ├── application/services          # 유즈케이스
│       ├── application/dtos              # DTO
│       ├── domain                        # 도메인 엔티티/리포지토리 인터페이스
│       └── infrastructure                # DB 모델, 리포지토리 구현
├── tests                             # 통합 테스트 (pytest + httpx)
└── docker/init.sql                   # docker-compose용 초기 SQL (app_test DB 생성)
```

## 개발 환경 준비

1. Poetry 설치 (없다면) : [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
2. 의존성 설치
   ```bash
   poetry install
   ```
3. 환경 변수 설정
   ```bash
   cp .env.example .env
   # 필요 시 DATABASE_URL 수정
   ```
4. 로컬 실행
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Ruff 린트

```bash
poetry run ruff check .
```

## 테스트 실행

```bash
poetry run pytest -q
```

## Docker 빌드 & 실행

```bash
# 이미지 빌드
docker build -t fastapi-clean .

# 단독 컨테이너 실행
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/app \
  fastapi-clean
```

## Docker Compose 예제

PostgreSQL, API 서버, 테스트 컨테이너까지 한 번에 기동합니다.

```bash
docker compose up --build
```

- `api` 서비스: FastAPI + Uvicorn
- `test` 서비스: 동일 이미지로 pytest 실행 (app_test 데이터베이스 사용)
- 로그 확인 후 테스트가 통과하면 `test` 컨테이너가 종료됩니다.

## API 간단 예시

- `POST /users/` : 사용자 생성 (email, full_name)
- `GET /users/` : 사용자 목록 조회
- `GET /health` : 헬스 체크

## 참고 사항

- 테스트는 `DATABASE_URL` 환경 변수로 지정된 DB를 사용합니다. docker-compose 실행 시 `app_test` 데이터베이스가 자동으로 생성됩니다.
- `Dockerfile`은 Poetry를 통해 의존성을 설치합니다. 네트워크가 가능한 환경에서 빌드를 수행해야 합니다.
