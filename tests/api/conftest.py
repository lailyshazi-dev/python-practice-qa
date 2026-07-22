import pytest

from src.api_client import ApiClient
from src.config import get_api_base_url, get_api_token


@pytest.fixture(scope="module")
def api_client():
    client = ApiClient(get_api_base_url())

    yield client

    client.close()


@pytest.fixture
def authorized_api_client(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token")

    client = ApiClient(
        "https://example.com",
        token=get_api_token(),
    )

    yield client

    client.close()


@pytest.fixture
def new_post_payload():
    return {
        "title": "Test title",
        "body": "Test body",
        "userId": 1,
    }


@pytest.fixture
def updated_post_payload():
    return {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1,
    }


@pytest.fixture
def patched_post_payload():
    return {
        "title": "Patched title",
    }