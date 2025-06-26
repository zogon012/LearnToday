from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    is_done: Optional[bool] = None

class TodoInDB(TodoBase):
    id: int
    is_done: bool
    created_at: datetime

    class Config:
        orm_mode = True 