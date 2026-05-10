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
