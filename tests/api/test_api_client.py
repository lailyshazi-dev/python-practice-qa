import pytest
import requests


pytestmark = pytest.mark.api


def test_api_client_uses_requests_session(api_client):
    assert isinstance(api_client.session, requests.Session), (
        f"Expected requests.Session, got {type(api_client.session).__name__}"
    )


def test_api_client_has_default_accept_header(api_client):
    assert api_client.session.headers["Accept"] == "application/json"