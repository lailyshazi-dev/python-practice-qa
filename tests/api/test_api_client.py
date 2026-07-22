import pytest
import requests


pytestmark = pytest.mark.api


def test_api_client_uses_requests_session(api_client):
    assert isinstance(api_client.session, requests.Session), (
        f"Expected requests.Session, got {type(api_client.session).__name__}"
    )


def test_api_client_has_default_accept_header(api_client):
    assert api_client.session.headers["Accept"] == "application/json"


def test_api_client_close_calls_session_close(api_client, monkeypatch):
    close_calls = []

    def fake_close():
        close_calls.append("closed")

    monkeypatch.setattr(api_client.session, "close", fake_close)

    api_client.close()

    assert close_calls == ["closed"]


def test_api_client_adds_bearer_token_header(authorized_api_client):
    assert (
        authorized_api_client.session.headers["Authorization"]
        == "Bearer test-token"
    )


def test_api_client_without_token_has_no_authorization_header(api_client):
    assert "Authorization" not in api_client.session.headers


def test_get_sends_expected_request(api_client, monkeypatch):
    captured_request = {}
    expected_response = object()

    def fake_get(url, params, timeout):
        captured_request.update(
            {
                "url": url,
                "params": params,
                "timeout": timeout,
            }
        )
        return expected_response

    monkeypatch.setattr(api_client.session, "get", fake_get)

    response = api_client.get(
        "/posts",
        params={"userId": 1},
    )

    assert response is expected_response
    assert captured_request == {
        "url": f"{api_client.base_url}/posts",
        "params": {"userId": 1},
        "timeout": api_client.timeout,
    }


def test_get_post_uses_expected_path(api_client, monkeypatch):
    captured_calls = []
    expected_response = object()

    def fake_get(path, params=None):
        captured_calls.append(
            {
                "path": path,
                "params": params,
            }
        )
        return expected_response

    monkeypatch.setattr(api_client, "get", fake_get)

    response = api_client.get_post(7)

    assert response is expected_response
    assert captured_calls == [
        {
            "path": "/posts/7",
            "params": None,
        }
    ]
