from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from db_api.src.app import app


@pytest.mark.anyio
async def test_list_users():
    async with AsyncClient(app="app:app", base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
