from __future__ import annotations

from typing import Protocol, Sequence

from app.user.domain.entities.user import User


class UserRepository(Protocol):
    """Abstract repository defining user persistence operations."""

    async def create_user(self, *, email: str, full_name: str) -> User:
        """Persist a new user and return the resulting domain entity."""

    async def list_users(self) -> Sequence[User]:
        """Return all users ordered by creation time."""
