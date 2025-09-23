from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from app.application.services import PushNotificationService
from app.domain.entities import PushNotification


@dataclass
class CreatePushNotificationCommand:
    """푸시 알림 생성 명령"""
    user_id: str
    message: str
    topic: Optional[str] = None


@dataclass
class GetPushNotificationQuery:
    """푸시 알림 조회 쿼리"""
    push_uuid: UUID


@dataclass
class GetUserPushNotificationsQuery:
    """사용자별 푸시 알림 목록 조회 쿼리"""
    user_id: str
    limit: int = 10


@dataclass
class GetTopicPushNotificationsQuery:
    """토픽별 푸시 알림 목록 조회 쿼리"""
    topic: str
    limit: int = 10


@dataclass
class DeletePushNotificationCommand:
    """푸시 알림 삭제 명령"""
    push_uuid: UUID


class CreatePushNotificationUseCase:
    """푸시 알림 생성 유스케이스"""

    def __init__(self, push_service: PushNotificationService):
        self._push_service = push_service

    async def execute(self, command: CreatePushNotificationCommand) -> PushNotification:
        """푸시 알림 생성 실행"""
        return await self._push_service.create_push_notification(
            user_id=command.user_id,
            message=command.message,
            topic=command.topic
        )


class GetPushNotificationUseCase:
    """푸시 알림 조회 유스케이스"""

    def __init__(self, push_service: PushNotificationService):
        self._push_service = push_service

    async def execute(self, query: GetPushNotificationQuery) -> Optional[PushNotification]:
        """푸시 알림 조회 실행"""
        return await self._push_service.get_push_notification(query.push_uuid)


class GetUserPushNotificationsUseCase:
    """사용자별 푸시 알림 목록 조회 유스케이스"""

    def __init__(self, push_service: PushNotificationService):
        self._push_service = push_service

    async def execute(self, query: GetUserPushNotificationsQuery) -> List[PushNotification]:
        """사용자별 푸시 알림 목록 조회 실행"""
        return await self._push_service.get_user_push_notifications(
            user_id=query.user_id,
            limit=query.limit
        )


class GetTopicPushNotificationsUseCase:
    """토픽별 푸시 알림 목록 조회 유스케이스"""

    def __init__(self, push_service: PushNotificationService):
        self._push_service = push_service

    async def execute(self, query: GetTopicPushNotificationsQuery) -> List[PushNotification]:
        """토픽별 푸시 알림 목록 조회 실행"""
        return await self._push_service.get_topic_push_notifications(
            topic=query.topic,
            limit=query.limit
        )


class DeletePushNotificationUseCase:
    """푸시 알림 삭제 유스케이스"""

    def __init__(self, push_service: PushNotificationService):
        self._push_service = push_service

    async def execute(self, command: DeletePushNotificationCommand) -> bool:
        """푸시 알림 삭제 실행"""
        return await self._push_service.delete_push_notification(command.push_uuid)