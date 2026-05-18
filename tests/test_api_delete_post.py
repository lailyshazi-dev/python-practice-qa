import pytest


pytestmark = pytest.mark.api


def test_delete_post_status_code(api_client):
    response = api_client.delete_post(1)

    assert response.status_code == 200


def test_delete_post_returns_empty_body(api_client):
    response = api_client.delete_post(1)
    data = response.json()

    assert data == {}
