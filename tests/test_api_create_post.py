import pytest


pytestmark = pytest.mark.api


def test_create_post_status_code(api_client, new_post_payload):
    response = api_client.create_post(new_post_payload)

    assert response.status_code == 201


def test_create_post_response_contains_sent_data(api_client, new_post_payload):
    response = api_client.create_post(new_post_payload)
    data = response.json()

    assert data["title"] == new_post_payload["title"]
    assert data["body"] == new_post_payload["body"]
    assert data["userId"] == new_post_payload["userId"]
    assert "id" in data
