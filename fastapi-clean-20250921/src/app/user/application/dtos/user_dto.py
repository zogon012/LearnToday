from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    email: EmailStr
    full_name: str


class UserDTO(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserListDTO(BaseModel):
    users: List[UserDTO]
