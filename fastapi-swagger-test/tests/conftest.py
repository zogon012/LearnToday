import pytest
from fastapi.testclient import TestClient
from my_fastapi_project.main import app


@pytest.fixture
def client():
    return TestClient(app)
