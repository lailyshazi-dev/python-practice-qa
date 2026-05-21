import pytest


pytestmark = pytest.mark.api


def test_update_post_status_code(api_client, updated_post_payload):
    response = api_client.update_post(1, updated_post_payload)

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )


def test_update_post_response_contains_updated_data(api_client, updated_post_payload):
    response = api_client.update_post(1, updated_post_payload)
    data = response.json()

    assert data["id"] == updated_post_payload["id"], (
        f"Expected id {updated_post_payload['id']}, got {data['id']}"
    )
    assert data["title"] == updated_post_payload["title"], (
        f"Expected title {updated_post_payload['title']!r}, got {data['title']!r}"
    )
    assert data["body"] == updated_post_payload["body"], (
        f"Expected body {updated_post_payload['body']!r}, got {data['body']!r}"
    )
    assert data["userId"] == updated_post_payload["userId"], (
        f"Expected userId {updated_post_payload['userId']}, got {data['userId']}"
    )


def test_patch_post_status_code(api_client, patched_post_payload):
    response = api_client.patch_post(1, patched_post_payload)

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )


def test_patch_post_response_contains_updated_field(api_client, patched_post_payload):
    response = api_client.patch_post(1, patched_post_payload)
    data = response.json()

    assert data["id"] == 1, f"Expected post id 1, got {data['id']}"
    assert data["title"] == patched_post_payload["title"], (
        f"Expected title {patched_post_payload['title']!r}, got {data['title']!r}"
    )
