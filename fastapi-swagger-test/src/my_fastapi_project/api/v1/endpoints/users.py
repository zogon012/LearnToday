from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from ....schemas.user import User, UserCreate
from ....services.user import UserService
from ....dependencies import get_user_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="모든 사용자 조회",
    description="시스템에 등록된 모든 사용자의 목록을 반환합니다.",
)
async def read_users(
    user_service: UserService = Depends(get_user_service),
) -> List[User]:
    """
    모든 사용자의 목록을 조회합니다.

    Returns:
        List[User]: 사용자 목록
    """
    return user_service.get_users()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 사용자 생성",
    description="새로운 사용자를 시스템에 등록합니다.",
)
async def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
) -> User:
    """
    새로운 사용자를 생성합니다.

    Args:
        user (UserCreate): 생성할 사용자 정보

    Returns:
        User: 생성된 사용자 정보

    Raises:
        HTTPException: 이메일이 이미 존재하는 경우
    """
    return user_service.create_user(user)


@router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="특정 사용자 조회",
    description="주어진 ID에 해당하는 사용자의 정보를 반환합니다.",
)
async def read_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> User:
    """
    특정 사용자의 정보를 조회합니다.

    Args:
        user_id (int): 조회할 사용자의 ID

    Returns:
        User: 사용자 정보

    Raises:
        HTTPException: 사용자를 찾을 수 없는 경우
    """
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
