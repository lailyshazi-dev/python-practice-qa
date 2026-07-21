import pytest

from src.api_client import ApiClient


@pytest.fixture(scope="module")
def api_client():
    client = ApiClient("https://jsonplaceholder.typicode.com")

    yield client

    client.close()


@pytest.fixture
def authorized_api_client():
    client = ApiClient(
        "https://example.com",
        token="test-token",
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