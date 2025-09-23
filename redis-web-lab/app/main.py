import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.application.services import PushNotificationService
from app.infrastructure.database import RedisConnection
from app.infrastructure.repositories import RedisPushNotificationRepository
from app.presentation.api import health_router as health_api_router
from app.presentation.api import push_router as push_api_router
from app.presentation.api.health_router import get_redis_connection
from app.presentation.api.push_router import get_push_notification_service

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 전역 의존성
redis_connection = RedisConnection(
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379")
)
push_repository = RedisPushNotificationRepository(redis_connection)
push_service = PushNotificationService(push_repository)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    # 시작 시
    try:
        await redis_connection.connect()
        logger.info("애플리케이션 시작 완료")
    except Exception as e:
        logger.error(f"애플리케이션 시작 실패: {e}")
    
    yield
    
    # 종료 시
    try:
        await redis_connection.disconnect()
        logger.info("애플리케이션 종료 완료")
    except Exception as e:
        logger.error(f"애플리케이션 종료 중 오류: {e}")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Redis Web Lab API - Clean Architecture",
    description="FastAPI with Redis, RedisInsight, and Webdis integration using Clean Architecture",
    version=__version__,
    lifespan=lifespan
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서만 사용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 의존성 오버라이드
def override_redis_connection() -> RedisConnection:
    return redis_connection

def override_push_service() -> PushNotificationService:
    return push_service

# 의존성 주입 설정
app.dependency_overrides[get_redis_connection] = override_redis_connection
app.dependency_overrides[get_push_notification_service] = override_push_service

# 라우터 등록
app.include_router(health_api_router)
app.include_router(push_api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
