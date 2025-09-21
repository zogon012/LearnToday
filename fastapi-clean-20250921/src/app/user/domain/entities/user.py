from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class User:
    """Domain entity representing a user."""

    id: UUID
    email: str
    full_name: str
    created_at: datetime
