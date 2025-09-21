from __future__ import annotations

from app.user.application.dtos.user_dto import UserCreateDTO, UserDTO, UserListDTO
from app.user.application.services.user_service import UserService
from app.user.infrastructure.db.session import get_session
from app.user.infrastructure.repositories.user_repository_impl import SqlAlchemyUserRepository
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    repository = SqlAlchemyUserRepository(session)
    return UserService(repository)


@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreateDTO, service: UserService = Depends(get_user_service)) -> UserDTO:
    try:
        return await service.create_user(payload)
    except ValueError as exc:  # pragma: no cover - simple mapping
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=UserListDTO)
async def list_users(service: UserService = Depends(get_user_service)) -> UserListDTO:
    return await service.list_users()
