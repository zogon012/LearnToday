# Redis Web Lab - Clean Architecture

Redis, RedisInsight, Webdis를 활용한 FastAPI 기반 푸시 알림 시스템입니다. Clean Architecture 패턴을 적용하여 구현되었습니다.

## 아키텍처

이 프로젝트는 Clean Architecture 원칙을 따라 다음과 같이 구성되어 있습니다:

```
app/
├── domain/                 # 도메인 레이어 (비즈니스 로직)
│   ├── entities/          # 도메인 엔티티
│   └── repositories/      # 저장소 인터페이스
├── application/           # 애플리케이션 레이어 (유스케이스)
│   ├── services/         # 애플리케이션 서비스
│   └── use_cases/        # 유스케이스
├── infrastructure/       # 인프라스트럭처 레이어 (외부 의존성)
│   ├── database/         # 데이터베이스 연결
│   └── repositories/     # 저장소 구현체
└── presentation/         # 프레젠테이션 레이어 (API)
    ├── api/             # API 라우터
    └── schemas/         # 요청/응답 스키마
```

## 주요 기능

- **푸시 알림 생성**: 사용자별 푸시 알림 생성 및 UUID 할당
- **API 호출 시간 기록**: 모든 API 호출 시간을 JSON 형태로 Redis에 저장
- **토픽 기반 분류**: 사용자 정의 토픽 또는 기본 토픽으로 알림 분류
- **Redis 기반 저장소**: 빠른 읽기/쓰기를 위한 Redis 활용
- **Clean Architecture**: 계층화된 아키텍처로 유지보수성 향상

## 기술 스택

- **Backend**: FastAPI, Python 3.11
- **Database**: Redis 7.x
- **Tools**: RedisInsight (GUI), Webdis (HTTP API)
- **Containerization**: Docker, Docker Compose
- **Dependency Management**: Poetry
- **Code Quality**: Ruff, Black, MyPy, Pre-commit hooks
- **Testing**: Pytest, Pytest-asyncio

## 사전 요구사항

- Python 3.11+
- Poetry
- Docker & Docker Compose
- Git

## 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd redis-web-lab
```

### 2. Poetry로 의존성 설치

```bash
poetry install
```

### 3. Pre-commit 훅 설치

```bash
poetry run pre-commit install
```

### 4. Docker Compose로 전체 스택 실행

```bash
# 프로덕션 모드
docker-compose up -d

# 개발 모드 (핫 리로드)
docker-compose --profile dev up -d
```

### 5. 로컬 개발 환경 실행

```bash
# Redis만 실행
docker-compose up redis -d

# FastAPI 애플리케이션 실행
poetry run python -m app.main
```

## 서비스 접근

- **FastAPI API**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **RedisInsight**: http://localhost:8001
- **Webdis HTTP API**: http://localhost:7379
- **개발용 API** (핫 리로드): http://localhost:8002

## API 엔드포인트

### 헬스체크
- `GET /` - 서비스 정보
- `GET /health` - 서비스 상태 및 Redis 연결 확인

### 푸시 알림
- `POST /push` - 푸시 알림 생성
- `GET /push/{push_uuid}` - 푸시 알림 조회
- `DELETE /push/{push_uuid}` - 푸시 알림 삭제
- `GET /push/user/{user_id}/pushes` - 사용자별 푸시 목록 조회
- `GET /push/topic/{topic}/pushes` - 토픽별 푸시 목록 조회

### 요청 예시

#### 푸시 알림 생성
```bash
curl -X POST http://localhost:8000/push \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "안녕하세요!",
    "topic": "notification"
  }'
```

## 테스트

### 전체 테스트 실행
```bash
poetry run pytest
```

### 커버리지 포함 테스트
```bash
poetry run pytest --cov=app --cov-report=html
```

### 특정 테스트 파일 실행
```bash
poetry run pytest tests/test_api.py -v
```

## 코드 품질 검사

### 수동 실행
```bash
# Ruff 린팅
poetry run ruff check app tests

# Black 포맷팅 검사
poetry run black --check app tests

# MyPy 타입 검사
poetry run mypy app

# 모든 검사 실행
./scripts/check.sh
```

### Pre-commit 훅으로 자동 실행
```bash
# 커밋 시 자동으로 실행됩니다
git commit -m "feat: add new feature"
```

## Docker 명령어

### 이미지 빌드
```bash
docker build -t redis-web-lab .
```

### 개별 서비스 실행
```bash
# Redis 실행
docker-compose up redis -d

# RedisInsight 실행
docker-compose up redisinsight -d

# Webdis 실행
docker-compose up webdis -d

# FastAPI 실행
docker-compose up api -d
```

### 로그 확인
```bash
docker-compose logs -f api
```

### 컨테이너 정리
```bash
docker-compose down -v
```

## 모니터링 도구

### RedisInsight
- URL: http://localhost:8001
- Redis 데이터를 시각적으로 탐색하고 관리
- Connection URL: `redis://redis:6379`
  1. RedisInsight에 접속 후 **Add Database** 선택
  2. Connection URL 입력란에 `redis://redis:6379` 입력
  3. Name 등 표시용 정보를 원하는 값으로 입력하고 저장
- 키 구조: 메시지는 `hash`(`push:{uuid}`)로 저장되고 TTL은 60초입니다. 사용자/토픽별 집합은 `set`(`user_pushes:{userId}`, `topic_pushes:{topic}`)로 관리하여 빠른 조회를 지원합니다.

### Webdis
- URL: http://localhost:7379
- Redis 명령어를 HTTP API로 실행
- 예시: `GET http://localhost:7379/GET/push:uuid`

## 개발 가이드

### 새로운 기능 추가

1. **Domain Layer**: 새로운 엔티티와 비즈니스 규칙 정의
2. **Application Layer**: 유스케이스와 서비스 구현
3. **Infrastructure Layer**: 외부 시스템과의 연동 구현
4. **Presentation Layer**: API 엔드포인트와 스키마 정의

### 코드 스타일 가이드

- Python 코드: PEP 8 준수, Black 포맷터 사용
- 타입 힌트: 모든 함수와 메서드에 타입 힌트 추가
- 문서화: 모듈, 클래스, 함수에 독스트링 작성
- 테스트: 새로운 기능에 대한 테스트 코드 작성

## 환경 변수

- `REDIS_URL`: Redis 연결 URL (기본값: `redis://localhost:6379`)
- `PYTHONPATH`: Python 모듈 경로 (기본값: `/app`)

## 라이선스

이 프로젝트는 MIT 라이선스하에 배포됩니다.

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Clean Architecture를 통한 확장 가능하고 유지보수 가능한 API 시스템**
