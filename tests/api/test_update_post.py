import pytest


pytestmark = pytest.mark.api


def test_update_post_status_code(api_client, updated_post_payload):
    response = api_client.update_post(1, updated_post_payload)

    assert response.status_code == 200


def test_update_post_response_contains_updated_data(api_client, updated_post_payload):
    response = api_client.update_post(1, updated_post_payload)
    data = response.json()

    assert data["id"] == updated_post_payload["id"]
    assert data["title"] == updated_post_payload["title"]
    assert data["body"] == updated_post_payload["body"]
    assert data["userId"] == updated_post_payload["userId"]


def test_patch_post_status_code(api_client, patched_post_payload):
    response = api_client.patch_post(1, patched_post_payload)

    assert response.status_code == 200


def test_patch_post_response_contains_updated_field(api_client, patched_post_payload):
    response = api_client.patch_post(1, patched_post_payload)
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == patched_post_payload["title"]
