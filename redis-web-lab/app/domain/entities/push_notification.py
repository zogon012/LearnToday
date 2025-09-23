from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class PushNotification:
    """푸시 알림 도메인 엔티티"""
    push_uuid: UUID
    user_id: str
    message: str
    topic: str
    created_at: datetime
    api_call_time: datetime
    status: str

    def __post_init__(self) -> None:
        """데이터 검증"""
        if not self.user_id.strip():
            raise ValueError("User ID cannot be empty")
        if not self.message.strip():
            raise ValueError("Message cannot be empty")
        if not self.topic.strip():
            raise ValueError("Topic cannot be empty")

    def is_active(self) -> bool:
        """활성 상태 확인"""
        return self.status in ["created", "sent", "delivered"]

    def mark_as_sent(self) -> None:
        """전송 완료로 상태 변경"""
        self.status = "sent"

    def mark_as_delivered(self) -> None:
        """전달 완료로 상태 변경"""
        self.status = "delivered"

    def mark_as_failed(self) -> None:
        """실패로 상태 변경"""
        self.status = "failed"

    @classmethod
    def create_new(
        cls,
        user_id: str,
        message: str,
        topic: Optional[str] = None,
        push_uuid: Optional[UUID] = None,
    ) -> "PushNotification":
        """새로운 푸시 알림 생성"""
        from uuid import uuid4
        
        if push_uuid is None:
            push_uuid = uuid4()
        
        if topic is None:
            topic = f"user_{user_id}_default"
        
        now = datetime.now()
        
        return cls(
            push_uuid=push_uuid,
            user_id=user_id,
            message=message,
            topic=topic,
            created_at=now,
            api_call_time=now,
            status="created"
        )