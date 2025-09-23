import logging
from typing import Optional

import redis.asyncio as redis
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RedisConnection:
    """Redis 연결 관리 클래스"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._redis: Optional[Redis] = None

    async def connect(self) -> None:
        """Redis에 연결"""
        try:
            self._redis = redis.from_url(
                self.redis_url, 
                encoding="utf-8", 
                decode_responses=True
            )
            await self._redis.ping()
            logger.info("Redis 연결 성공")
        except Exception as e:
            logger.error(f"Redis 연결 실패: {e}")
            raise

    async def disconnect(self) -> None:
        """Redis 연결 종료"""
        if self._redis:
            await self._redis.close()
            logger.info("Redis 연결 종료")

    async def is_connected(self) -> bool:
        """Redis 연결 상태 확인"""
        try:
            if self._redis:
                await self._redis.ping()
                return True
        except Exception as e:
            logger.error(f"Redis 연결 확인 실패: {e}")
        return False

    @property
    def client(self) -> Redis:
        """Redis 클라이언트 반환"""
        if not self._redis:
            raise Exception("Redis가 연결되지 않음")
        return self._redis