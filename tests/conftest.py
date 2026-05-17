import pytest
from src.api_client import ApiClient


@pytest.fixture(scope="function")
def sample_numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture(scope="module")
def calculator_config():
    return {
        "precision": 2,
        "mode": "standard",
    }


@pytest.fixture(scope="module")
def api_client():
    return ApiClient("https://jsonplaceholder.typicode.com")


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
