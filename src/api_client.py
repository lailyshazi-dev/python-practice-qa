import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
            }
        )

    def get(self, path: str, params: dict | None = None):
        return self.session.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
        )

    def get_post(self, post_id: int):
        return self.get(f"/posts/{post_id}")

    def get_posts(self):
        return self.get("/posts")

    def get_posts_by_user(self, user_id: int):
        return self.get("/posts", params={"userId": user_id})

    def get_posts_page(self, page: int, limit: int):
        return self.get(
            "/posts",
            params={"_page": page, "_limit": limit},
        )

    def post(self, path: str, json: dict):
        return self.session.post(f"{self.base_url}{path}", json=json, timeout=self.timeout)

    def create_post(self, payload: dict):
        return self.post("/posts", json=payload)

    def put(self, path: str, json: dict):
        return self.session.put(f"{self.base_url}{path}", json=json, timeout=self.timeout)

    def update_post(self, post_id: int, payload: dict):
        return self.put(f"/posts/{post_id}", json=payload)

    def patch(self, path: str, json: dict):
        return self.session.patch(f"{self.base_url}{path}", json=json, timeout=self.timeout)

    def patch_post(self, post_id: int, payload: dict):
        return self.patch(f"/posts/{post_id}", json=payload)

    def delete(self, path: str):
        return self.session.delete(f"{self.base_url}{path}", timeout=self.timeout)

    def delete_post(self, post_id: int):
        return self.delete(f"/posts/{post_id}")
