from fastapi import FastAPI
from app.routers import todo
from app.database import init_db
import asyncio

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(todo.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
