import logging
from typing import List, Optional
from uuid import UUID

from app.domain.entities import PushNotification
from app.domain.repositories import PushNotificationRepository
from app.infrastructure.database import RedisConnection

logger = logging.getLogger(__name__)


class RedisPushNotificationRepository(PushNotificationRepository):
    """Redis 기반 푸시 알림 저장소 구현체"""

    _TTL_SECONDS = 60

    def __init__(self, redis_connection: RedisConnection):
        self._redis_connection = redis_connection

    async def save(self, push_notification: PushNotification) -> bool:
        """푸시 알림 저장"""
        try:
            redis_client = self._redis_connection.client
            
            # 메인 데이터를 Hash로 저장
            key = f"push:{push_notification.push_uuid}"
            data = {
                "push_uuid": str(push_notification.push_uuid),
                "user_id": push_notification.user_id,
                "message": push_notification.message,
                "topic": push_notification.topic,
                "created_at": push_notification.created_at.isoformat(),
                "api_call_time": push_notification.api_call_time.isoformat(),
                "status": push_notification.status,
            }
            
            await redis_client.hset(key, mapping=data)
            
            # TTL 설정 (1분)
            await redis_client.expire(key, self._TTL_SECONDS)
            
            # 사용자별 인덱스 추가
            user_key = f"user_pushes:{push_notification.user_id}"
            await redis_client.sadd(user_key, str(push_notification.push_uuid))
            await redis_client.expire(user_key, self._TTL_SECONDS)
            
            # 토픽별 인덱스 추가
            topic_key = f"topic_pushes:{push_notification.topic}"
            await redis_client.sadd(topic_key, str(push_notification.push_uuid))
            await redis_client.expire(topic_key, self._TTL_SECONDS)
            
            logger.info(f"푸시 기록 저장 성공: {push_notification.push_uuid}")
            return True
        except Exception as e:
            logger.error(f"푸시 기록 저장 실패: {e}")
            return False

    async def find_by_id(self, push_uuid: UUID) -> Optional[PushNotification]:
        """ID로 푸시 알림 조회"""
        try:
            redis_client = self._redis_connection.client
            key = f"push:{push_uuid}"
            record_data = await redis_client.hgetall(key)
            
            if not record_data:
                return None
            
            return self._to_entity(record_data)
        except Exception as e:
            logger.error(f"푸시 기록 조회 실패: {e}")
            return None

    async def find_by_user_id(self, user_id: str, limit: int = 10) -> List[PushNotification]:
        """사용자 ID로 푸시 알림 목록 조회"""
        try:
            redis_client = self._redis_connection.client
            user_key = f"user_pushes:{user_id}"
            push_uuids = await redis_client.smembers(user_key)
            
            entities = []
            for push_uuid in list(push_uuids)[:limit]:
                entity = await self.find_by_id(UUID(push_uuid))
                if entity:
                    entities.append(entity)
            
            # 생성시간 기준 내림차순 정렬
            entities.sort(key=lambda x: x.created_at, reverse=True)
            return entities
        except Exception as e:
            logger.error(f"사용자 푸시 기록 조회 실패: {e}")
            return []

    async def find_by_topic(self, topic: str, limit: int = 10) -> List[PushNotification]:
        """토픽으로 푸시 알림 목록 조회"""
        try:
            redis_client = self._redis_connection.client
            topic_key = f"topic_pushes:{topic}"
            push_uuids = await redis_client.smembers(topic_key)
            
            entities = []
            for push_uuid in list(push_uuids)[:limit]:
                entity = await self.find_by_id(UUID(push_uuid))
                if entity:
                    entities.append(entity)
            
            # 생성시간 기준 내림차순 정렬
            entities.sort(key=lambda x: x.created_at, reverse=True)
            return entities
        except Exception as e:
            logger.error(f"토픽 푸시 기록 조회 실패: {e}")
            return []

    async def delete(self, push_uuid: UUID) -> bool:
        """푸시 알림 삭제"""
        try:
            # 먼저 기록을 조회해서 사용자와 토픽 정보를 얻음
            entity = await self.find_by_id(push_uuid)
            if not entity:
                return False

            redis_client = self._redis_connection.client
            
            # 메인 기록 삭제
            key = f"push:{push_uuid}"
            await redis_client.delete(key)
            
            # 인덱스에서도 제거
            user_key = f"user_pushes:{entity.user_id}"
            await redis_client.srem(user_key, str(push_uuid))
            
            topic_key = f"topic_pushes:{entity.topic}"
            await redis_client.srem(topic_key, str(push_uuid))
            
            logger.info(f"푸시 기록 삭제 성공: {push_uuid}")
            return True
        except Exception as e:
            logger.error(f"푸시 기록 삭제 실패: {e}")
            return False

    async def exists(self, push_uuid: UUID) -> bool:
        """푸시 알림 존재 여부 확인"""
        try:
            redis_client = self._redis_connection.client
            key = f"push:{push_uuid}"
            return await redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"푸시 기록 존재 확인 실패: {e}")
            return False

    def _to_entity(self, record_data: dict) -> PushNotification:
        """Redis 데이터를 Entity로 변환"""
        from datetime import datetime
        
        return PushNotification(
            push_uuid=UUID(record_data["push_uuid"]),
            user_id=record_data["user_id"],
            message=record_data["message"],
            topic=record_data["topic"],
            created_at=datetime.fromisoformat(record_data["created_at"]),
            api_call_time=datetime.fromisoformat(record_data["api_call_time"]),
            status=record_data["status"],
        )
