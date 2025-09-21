from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.user.api.v1.routes.users import router as user_router
from app.user.infrastructure.db.session import init_models


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_models()
    yield


app = FastAPI(title="FastAPI Clean Architecture", lifespan=lifespan)
app.include_router(user_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
