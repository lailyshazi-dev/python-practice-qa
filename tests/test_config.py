from src.config import get_api_token


def test_get_api_token_returns_environment_value(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "test-token")

    assert get_api_token() == "test-token"


def test_get_api_token_returns_none_when_missing(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)

    assert get_api_token() is None