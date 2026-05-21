import pytest


pytestmark = pytest.mark.api


def test_create_post_status_code(api_client, new_post_payload):
    response = api_client.create_post(new_post_payload)

    assert response.status_code == 201, (
        f"Expected status code 201, got {response.status_code}"
    )


def test_create_post_response_contains_sent_data(api_client, new_post_payload):
    response = api_client.create_post(new_post_payload)
    data = response.json()

    assert data["title"] == new_post_payload["title"], (
        f"Expected title {new_post_payload['title']!r}, got {data['title']!r}"
    )
    assert data["body"] == new_post_payload["body"], (
        f"Expected body {new_post_payload['body']!r}, got {data['body']!r}"
    )
    assert data["userId"] == new_post_payload["userId"], (
        f"Expected userId {new_post_payload['userId']}, got {data['userId']}"
    )
    assert "id" in data, "Created post response should contain field 'id'"
