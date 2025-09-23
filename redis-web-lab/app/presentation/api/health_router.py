from datetime import datetime

from fastapi import APIRouter, Depends

from app.infrastructure.database import RedisConnection
from app.presentation.schemas import HealthResponse
from app import __version__

router = APIRouter(tags=["Health"])


def get_redis_connection() -> RedisConnection:
    """Redis 연결 의존성 주입"""
    # 이는 main.py에서 오버라이드됩니다
    raise NotImplementedError


@router.get("/", response_model=dict)
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Redis Web Lab API - Clean Architecture",
        "version": __version__,
        "timestamp": datetime.now(),
        "architecture": "Clean Architecture with Domain-Driven Design"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check(redis_connection: RedisConnection = Depends(get_redis_connection)):
    """헬스체크 엔드포인트"""
    redis_connected = await redis_connection.is_connected()
    
    return HealthResponse(
        status="healthy" if redis_connected else "unhealthy",
        timestamp=datetime.now(),
        redis_connected=redis_connected,
        version=__version__
    )