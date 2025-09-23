from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities import PushNotification


class PushNotificationRepository(ABC):
    """푸시 알림 저장소 인터페이스"""

    @abstractmethod
    async def save(self, push_notification: PushNotification) -> bool:
        """푸시 알림 저장"""
        pass

    @abstractmethod
    async def find_by_id(self, push_uuid: UUID) -> Optional[PushNotification]:
        """ID로 푸시 알림 조회"""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str, limit: int = 10) -> List[PushNotification]:
        """사용자 ID로 푸시 알림 목록 조회"""
        pass

    @abstractmethod
    async def find_by_topic(self, topic: str, limit: int = 10) -> List[PushNotification]:
        """토픽으로 푸시 알림 목록 조회"""
        pass

    @abstractmethod
    async def delete(self, push_uuid: UUID) -> bool:
        """푸시 알림 삭제"""
        pass

    @abstractmethod
    async def exists(self, push_uuid: UUID) -> bool:
        """푸시 알림 존재 여부 확인"""
        pass