from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import TodoCreate, TodoUpdate, TodoInDB
from app.crud import create_todo, get_todo, get_todos, update_todo, delete_todo
from app.database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create(todo_in: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo(db, todo_in)

@router.get("/", response_model=List[TodoInDB])
async def read_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_todos(db, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model=TodoInDB)
async def read_one(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoInDB)
async def update(todo_id: int, todo_in: TodoUpdate, db: AsyncSession = Depends(get_db)):
    todo = await update_todo(db, todo_id, todo_in)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(todo_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None 