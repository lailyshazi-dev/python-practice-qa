import pytest
import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, path: str):
        return requests.get(f"{self.base_url}{path}", timeout=self.timeout)

    def get_post(self, post_id: int):
        return self.get(f"/posts/{post_id}")

    def get_posts(self):
        return self.get("/posts")


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

