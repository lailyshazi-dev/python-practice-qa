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
