from __future__ import annotations

import pytest
from app.main import app
from app.user.infrastructure.db.models import Base
from app.user.infrastructure.db.session import engine
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
async def _reset_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app, lifespan="auto")
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
