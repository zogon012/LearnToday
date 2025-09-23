import pytest
import pytest_asyncio
from httpx import AsyncClient
import redis.asyncio as redis
from app.main import app
from app.redis_service import RedisService
import os


# 테스트용 Redis URL
TEST_REDIS_URL = os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")


@pytest_asyncio.fixture
async def test_redis_service():
    """테스트용 Redis 서비스 픽스처"""
    service = RedisService(redis_url=TEST_REDIS_URL)
    await service.connect()
    yield service
    
    # 테스트 데이터 정리
    if service._redis:
        await service._redis.flushdb()
        await service.disconnect()


@pytest_asyncio.fixture
async def async_client():
    """비동기 HTTP 클라이언트 픽스처"""
    # 테스트용 Redis URL로 오버라이드
    app.dependency_overrides = {}
    
    async def override_redis_service():
        service = RedisService(redis_url=TEST_REDIS_URL)
        await service.connect()
        return service
    
    from app.main import get_redis_service
    app.dependency_overrides[get_redis_service] = override_redis_service
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # 클리너업
    redis_service = await override_redis_service()
    if redis_service._redis:
        await redis_service._redis.flushdb()
        await redis_service.disconnect()
    
    app.dependency_overrides.clear()