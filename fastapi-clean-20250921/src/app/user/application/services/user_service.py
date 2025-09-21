from __future__ import annotations

from app.user.application.dtos.user_dto import UserCreateDTO, UserDTO, UserListDTO
from app.user.domain.repositories.user_repository import UserRepository


class UserService:
    """Application service coordinating user use cases."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def create_user(self, payload: UserCreateDTO) -> UserDTO:
        user = await self._repository.create_user(email=payload.email, full_name=payload.full_name)
        return UserDTO.model_validate(user)

    async def list_users(self) -> UserListDTO:
        users = await self._repository.list_users()
        items = [UserDTO.model_validate(user) for user in users]
        return UserListDTO(users=items)
