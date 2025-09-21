from __future__ import annotations

from typing import Sequence

from app.user.domain.entities.user import User
from app.user.domain.repositories.user_repository import UserRepository
from app.user.infrastructure.db.models import UserModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of the user repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_user(self, *, email: str, full_name: str) -> User:
        model = UserModel(email=email, full_name=full_name)
        self._session.add(model)
        try:
            await self._session.flush()
            await self._session.commit()
        except IntegrityError as exc:  # pragma: no cover - simple translation
            await self._session.rollback()
            raise ValueError("User with this email already exists") from exc
        await self._session.refresh(model)
        return self._to_domain(model)

    async def list_users(self) -> Sequence[User]:
        statement = select(UserModel).order_by(UserModel.created_at.asc())
        result = await self._session.execute(statement)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(id=model.id, email=model.email, full_name=model.full_name, created_at=model.created_at)
