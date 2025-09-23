from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserPushRequest(BaseModel):
    """사용자 푸시 요청 스키마"""
    user_id: str = Field(..., description="사용자 ID", min_length=1)
    message: str = Field(..., description="푸시 메시지", min_length=1)
    topic: Optional[str] = Field(None, description="토픽 (선택사항)")


class UserPushResponse(BaseModel):
    """사용자 푸시 응답 스키마"""
    push_uuid: UUID = Field(..., description="생성된 푸시 UUID")
    user_id: str = Field(..., description="사용자 ID")
    message: str = Field(..., description="푸시 메시지")
    topic: str = Field(..., description="토픽")
    created_at: datetime = Field(..., description="생성 시간")
    status: str = Field(..., description="푸시 상태")


class PushNotificationResponse(BaseModel):
    """푸시 알림 응답 스키마"""
    push_uuid: UUID = Field(..., description="푸시 UUID")
    user_id: str = Field(..., description="사용자 ID")
    message: str = Field(..., description="푸시 메시지")
    topic: str = Field(..., description="토픽")
    created_at: datetime = Field(..., description="생성 시간")
    api_call_time: datetime = Field(..., description="API 호출 시간")
    status: str = Field(..., description="푸시 상태")


class HealthResponse(BaseModel):
    """헬스체크 응답 스키마"""
    status: str = Field(..., description="서비스 상태")
    timestamp: datetime = Field(..., description="확인 시간")
    redis_connected: bool = Field(..., description="Redis 연결 상태")
    version: str = Field(..., description="애플리케이션 버전")


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 에러 메시지")