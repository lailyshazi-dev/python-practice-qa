import os


def get_api_token() -> str | None:
    return os.getenv("API_TOKEN")