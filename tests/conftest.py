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

