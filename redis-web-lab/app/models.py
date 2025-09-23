from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UserPushRequest(BaseModel):
    """사용자 푸시 요청 모델"""
    user_id: str = Field(..., description="사용자 ID")
    message: str = Field(..., description="푸시 메시지")
    topic: Optional[str] = Field(None, description="토픽 (선택사항)")


class UserPushResponse(BaseModel):
    """사용자 푸시 응답 모델"""
    push_uuid: UUID = Field(..., description="생성된 푸시 UUID")
    user_id: str = Field(..., description="사용자 ID")
    message: str = Field(..., description="푸시 메시지")
    topic: str = Field(..., description="토픽")
    created_at: datetime = Field(..., description="생성 시간")
    status: str = Field(..., description="푸시 상태")


class PushRecord(BaseModel):
    """Redis에 저장되는 푸시 기록"""
    push_uuid: str
    user_id: str
    message: str
    topic: str
    created_at: str
    api_call_time: str
    status: str


class HealthResponse(BaseModel):
    """헬스체크 응답 모델"""
    status: str
    timestamp: datetime
    redis_connected: bool
    version: str