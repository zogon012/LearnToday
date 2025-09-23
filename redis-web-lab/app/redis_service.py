import json
import logging
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import redis.asyncio as redis
from redis.asyncio import Redis

from app.models import PushRecord

logger = logging.getLogger(__name__)


class RedisService:
    """Redis 서비스 클래스"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._redis: Optional[Redis] = None

    async def connect(self) -> None:
        """Redis에 연결"""
        try:
            self._redis = redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
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

    async def save_push_record(self, record: PushRecord) -> bool:
        """푸시 기록을 Redis에 저장"""
        try:
            if not self._redis:
                raise Exception("Redis가 연결되지 않음")

            # JSON으로 직렬화하여 저장
            record_data = record.model_dump()
            key = f"push:{record.push_uuid}"
            
            # Hash로 저장
            await self._redis.hset(key, mapping=record_data)
            
            # TTL 설정 (7일)
            await self._redis.expire(key, 604800)
            
            # 사용자별 인덱스 추가
            user_key = f"user_pushes:{record.user_id}"
            await self._redis.sadd(user_key, record.push_uuid)
            await self._redis.expire(user_key, 604800)
            
            # 토픽별 인덱스 추가
            topic_key = f"topic_pushes:{record.topic}"
            await self._redis.sadd(topic_key, record.push_uuid)
            await self._redis.expire(topic_key, 604800)
            
            logger.info(f"푸시 기록 저장 성공: {record.push_uuid}")
            return True
        except Exception as e:
            logger.error(f"푸시 기록 저장 실패: {e}")
            return False

    async def get_push_record(self, push_uuid: str) -> Optional[PushRecord]:
        """푸시 기록을 UUID로 조회"""
        try:
            if not self._redis:
                raise Exception("Redis가 연결되지 않음")

            key = f"push:{push_uuid}"
            record_data = await self._redis.hgetall(key)
            
            if not record_data:
                return None
                
            return PushRecord(**record_data)
        except Exception as e:
            logger.error(f"푸시 기록 조회 실패: {e}")
            return None

    async def get_user_pushes(self, user_id: str, limit: int = 10) -> List[PushRecord]:
        """사용자의 푸시 기록 목록 조회"""
        try:
            if not self._redis:
                raise Exception("Redis가 연결되지 않음")

            user_key = f"user_pushes:{user_id}"
            push_uuids = await self._redis.smembers(user_key)
            
            records = []
            for push_uuid in list(push_uuids)[:limit]:
                record = await self.get_push_record(push_uuid)
                if record:
                    records.append(record)
            
            # 생성시간 기준 내림차순 정렬
            records.sort(key=lambda x: x.created_at, reverse=True)
            return records
        except Exception as e:
            logger.error(f"사용자 푸시 기록 조회 실패: {e}")
            return []

    async def get_topic_pushes(self, topic: str, limit: int = 10) -> List[PushRecord]:
        """토픽별 푸시 기록 목록 조회"""
        try:
            if not self._redis:
                raise Exception("Redis가 연결되지 않음")

            topic_key = f"topic_pushes:{topic}"
            push_uuids = await self._redis.smembers(topic_key)
            
            records = []
            for push_uuid in list(push_uuids)[:limit]:
                record = await self.get_push_record(push_uuid)
                if record:
                    records.append(record)
            
            # 생성시간 기준 내림차순 정렬
            records.sort(key=lambda x: x.created_at, reverse=True)
            return records
        except Exception as e:
            logger.error(f"토픽 푸시 기록 조회 실패: {e}")
            return []

    async def delete_push_record(self, push_uuid: str) -> bool:
        """푸시 기록 삭제"""
        try:
            if not self._redis:
                raise Exception("Redis가 연결되지 않음")

            # 먼저 기록을 조회해서 사용자와 토픽 정보를 얻음
            record = await self.get_push_record(push_uuid)
            if not record:
                return False

            # 메인 기록 삭제
            key = f"push:{push_uuid}"
            await self._redis.delete(key)
            
            # 인덱스에서도 제거
            user_key = f"user_pushes:{record.user_id}"
            await self._redis.srem(user_key, push_uuid)
            
            topic_key = f"topic_pushes:{record.topic}"
            await self._redis.srem(topic_key, push_uuid)
            
            logger.info(f"푸시 기록 삭제 성공: {push_uuid}")
            return True
        except Exception as e:
            logger.error(f"푸시 기록 삭제 실패: {e}")
            return False