from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services import PushNotificationService
from app.application.use_cases import (
    CreatePushNotificationCommand,
    CreatePushNotificationUseCase,
    DeletePushNotificationCommand, 
    DeletePushNotificationUseCase,
    GetPushNotificationQuery,
    GetPushNotificationUseCase,
    GetTopicPushNotificationsQuery,
    GetTopicPushNotificationsUseCase,
    GetUserPushNotificationsQuery,
    GetUserPushNotificationsUseCase,
)
from app.domain.entities import PushNotification
from app.presentation.schemas import (
    ErrorResponse,
    PushNotificationResponse,
    UserPushRequest,
    UserPushResponse,
)

router = APIRouter(prefix="/push", tags=["Push Notifications"])


def get_push_notification_service() -> PushNotificationService:
    """푸시 알림 서비스 의존성 주입"""
    # 이는 main.py에서 오버라이드됩니다
    raise NotImplementedError


def _to_push_response(entity: PushNotification) -> PushNotificationResponse:
    """엔티티를 응답 스키마로 변환"""
    return PushNotificationResponse(
        push_uuid=entity.push_uuid,
        user_id=entity.user_id,
        message=entity.message,
        topic=entity.topic,
        created_at=entity.created_at,
        api_call_time=entity.api_call_time,
        status=entity.status,
    )


@router.post("", response_model=UserPushResponse)
async def create_push(
    request: UserPushRequest,
    push_service: PushNotificationService = Depends(get_push_notification_service)
):
    """푸시 알림 생성"""
    try:
        use_case = CreatePushNotificationUseCase(push_service)
        command = CreatePushNotificationCommand(
            user_id=request.user_id,
            message=request.message,
            topic=request.topic
        )
        
        entity = await use_case.execute(command)
        
        return UserPushResponse(
            push_uuid=entity.push_uuid,
            user_id=entity.user_id,
            message=entity.message,
            topic=entity.topic,
            created_at=entity.created_at,
            status=entity.status,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="푸시 생성 실패"
        )


@router.get("/{push_uuid}", response_model=PushNotificationResponse)
async def get_push(
    push_uuid: UUID,
    push_service: PushNotificationService = Depends(get_push_notification_service)
):
    """푸시 알림 조회"""
    try:
        use_case = GetPushNotificationUseCase(push_service)
        query = GetPushNotificationQuery(push_uuid=push_uuid)
        
        entity = await use_case.execute(query)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="푸시 알림을 찾을 수 없습니다"
            )
        
        return _to_push_response(entity)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="푸시 조회 실패"
        )


@router.delete("/{push_uuid}")
async def delete_push(
    push_uuid: UUID,
    push_service: PushNotificationService = Depends(get_push_notification_service)
):
    """푸시 알림 삭제"""
    try:
        use_case = DeletePushNotificationUseCase(push_service)
        command = DeletePushNotificationCommand(push_uuid=push_uuid)
        
        success = await use_case.execute(command)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="푸시 알림을 찾을 수 없습니다"
            )
        
        return {"message": "푸시 알림이 성공적으로 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="푸시 삭제 실패"
        )


@router.get("/user/{user_id}/pushes", response_model=List[PushNotificationResponse])
async def get_user_pushes(
    user_id: str,
    limit: int = 10,
    push_service: PushNotificationService = Depends(get_push_notification_service)
):
    """사용자별 푸시 알림 목록 조회"""
    try:
        use_case = GetUserPushNotificationsUseCase(push_service)
        query = GetUserPushNotificationsQuery(user_id=user_id, limit=limit)
        
        entities = await use_case.execute(query)
        return [_to_push_response(entity) for entity in entities]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 푸시 목록 조회 실패"
        )


@router.get("/topic/{topic}/pushes", response_model=List[PushNotificationResponse])
async def get_topic_pushes(
    topic: str,
    limit: int = 10,
    push_service: PushNotificationService = Depends(get_push_notification_service)
):
    """토픽별 푸시 알림 목록 조회"""
    try:
        use_case = GetTopicPushNotificationsUseCase(push_service)
        query = GetTopicPushNotificationsQuery(topic=topic, limit=limit)
        
        entities = await use_case.execute(query)
        return [_to_push_response(entity) for entity in entities]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="토픽 푸시 목록 조회 실패"
        )