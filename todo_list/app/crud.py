from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, asc
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


async def create_todo(db: AsyncSession, todo_in: TodoCreate) -> Todo:
    todo = Todo(**todo_in.dict())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def get_todo(db: AsyncSession, todo_id: int) -> Todo | None:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Todo]:
    result = await db.execute(
        select(Todo).order_by(asc(Todo.id)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_todo(
    db: AsyncSession, todo_id: int, todo_in: TodoUpdate
) -> Todo | None:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        return None
    for field, value in todo_in.dict(exclude_unset=True).items():
        setattr(todo, field, value)
    await db.commit()
    await db.refresh(todo)
    return todo


async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        return False
    await db.delete(todo)
    await db.commit()
    return True
