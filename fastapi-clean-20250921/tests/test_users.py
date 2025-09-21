from __future__ import annotations

from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_create_user(async_client):
    payload = {"email": f"{uuid4()}@example.com", "full_name": "Test User"}
    response = await async_client.post("/users/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == payload["email"]
    assert body["full_name"] == payload["full_name"]


@pytest.mark.asyncio
async def test_duplicate_email_is_rejected(async_client):
    email = f"{uuid4()}@example.com"
    payload = {"email": email, "full_name": "Test User"}
    first = await async_client.post("/users/", json=payload)
    assert first.status_code == 201

    second = await async_client.post("/users/", json=payload)
    assert second.status_code == 400
    assert second.json()["detail"] == "User with this email already exists"


@pytest.mark.asyncio
async def test_list_users(async_client):
    email = f"{uuid4()}@example.com"
    payload = {"email": email, "full_name": "Test User"}
    await async_client.post("/users/", json=payload)

    response = await async_client.get("/users/")
    assert response.status_code == 200
    body = response.json()
    assert len(body["users"]) == 1
    assert body["users"][0]["email"] == email
