from src.config import (
    DEFAULT_API_BASE_URL,
    get_api_base_url,
    get_api_token,
)


def test_get_api_token_returns_environment_value(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token")

    assert get_api_token() == "test-token"


def test_get_api_token_returns_none_when_missing(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)

    assert get_api_token() is None


def test_get_api_base_url_returns_environment_value(monkeypatch):
    monkeypatch.setenv(
        "API_BASE_URL",
        "https://stage-api.example.com",
    )

    assert get_api_base_url() == "https://stage-api.example.com"


def test_get_api_base_url_returns_default_when_missing(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)

    assert get_api_base_url() == DEFAULT_API_BASE_URL
