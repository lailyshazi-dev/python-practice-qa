import pytest


pytestmark = pytest.mark.api


def test_get_post_by_id_status_code(api_client):
    response = api_client.get_post(1)

    assert response.status_code == 200


def test_get_post_by_id_has_expected_fields(api_client):
    response = api_client.get_post(1)
    data = response.json()

    assert "userId" in data
    assert "id" in data
    assert "title" in data
    assert "body" in data


def test_get_post_by_id_has_expected_id(api_client):
    response = api_client.get_post(1)
    data = response.json()

    assert data["id"] == 1


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post_by_id_parametrized(api_client, post_id):
    response = api_client.get_post(post_id)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == post_id


@pytest.mark.negative
def test_get_missing_post_returns_404(api_client):
    response = api_client.get_post(999999)

    assert response.status_code == 404


@pytest.mark.negative
def test_get_missing_post_returns_empty_body(api_client):
    response = api_client.get_post(999999)
    data = response.json()

    assert data == {}


def test_get_posts_status_code(api_client):
    response = api_client.get_posts()

    assert response.status_code == 200


def test_get_posts_returns_list(api_client):
    response = api_client.get_posts()
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_posts_items_have_expected_fields(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert "userId" in post
        assert "id" in post
        assert "title" in post
        assert "body" in post


def test_get_posts_items_have_expected_types(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_get_posts_response_time_is_within_timeout(api_client):
    response = api_client.get_posts()

    assert response.elapsed.total_seconds() < api_client.timeout


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


def test_delete_post_status_code(api_client):
    response = api_client.delete_post(1)

    assert response.status_code == 200


def test_delete_post_returns_empty_body(api_client):
    response = api_client.delete_post(1)
    data = response.json()

    assert data == {}
