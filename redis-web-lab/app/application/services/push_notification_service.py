from typing import List, Optional
from uuid import UUID

from app.domain.entities import PushNotification
from app.domain.repositories import PushNotificationRepository


class PushNotificationService:
    """푸시 알림 애플리케이션 서비스"""

    def __init__(self, push_repository: PushNotificationRepository):
        self._push_repository = push_repository

    async def create_push_notification(
        self, 
        user_id: str, 
        message: str, 
        topic: Optional[str] = None
    ) -> PushNotification:
        """새로운 푸시 알림 생성"""
        push_notification = PushNotification.create_new(
            user_id=user_id,
            message=message,
            topic=topic
        )
        
        success = await self._push_repository.save(push_notification)
        if not success:
            raise Exception("Failed to save push notification")
        
        return push_notification

    async def get_push_notification(self, push_uuid: UUID) -> Optional[PushNotification]:
        """푸시 알림 조회"""
        return await self._push_repository.find_by_id(push_uuid)

    async def get_user_push_notifications(
        self, 
        user_id: str, 
        limit: int = 10
    ) -> List[PushNotification]:
        """사용자별 푸시 알림 목록 조회"""
        if limit > 100:
            limit = 100
        return await self._push_repository.find_by_user_id(user_id, limit)

    async def get_topic_push_notifications(
        self, 
        topic: str, 
        limit: int = 10
    ) -> List[PushNotification]:
        """토픽별 푸시 알림 목록 조회"""
        if limit > 100:
            limit = 100
        return await self._push_repository.find_by_topic(topic, limit)

    async def delete_push_notification(self, push_uuid: UUID) -> bool:
        """푸시 알림 삭제"""
        exists = await self._push_repository.exists(push_uuid)
        if not exists:
            return False
        return await self._push_repository.delete(push_uuid)

    async def mark_push_as_sent(self, push_uuid: UUID) -> bool:
        """푸시 알림을 전송됨으로 표시"""
        push_notification = await self._push_repository.find_by_id(push_uuid)
        if not push_notification:
            return False
        
        push_notification.mark_as_sent()
        return await self._push_repository.save(push_notification)

    async def mark_push_as_delivered(self, push_uuid: UUID) -> bool:
        """푸시 알림을 전달됨으로 표시"""
        push_notification = await self._push_repository.find_by_id(push_uuid)
        if not push_notification:
            return False
        
        push_notification.mark_as_delivered()
        return await self._push_repository.save(push_notification)