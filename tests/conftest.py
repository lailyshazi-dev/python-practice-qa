import pytest
import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    def get_post(self, post_id: int):
        return requests.get(f"{self.base_url}/posts/{post_id}", timeout=self.timeout)

    def get_posts(self):
        return requests.get(f"{self.base_url}/posts", timeout=self.timeout)


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

