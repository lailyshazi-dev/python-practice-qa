import pytest


pytestmark = pytest.mark.api


def test_get_post_by_id_status_code(api_client):
    response = api_client.get_post(1)

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )


def test_get_post_by_id_has_expected_fields(api_client):
    response = api_client.get_post(1)
    data = response.json()

    assert "userId" in data, "Response should contain field 'userId'"
    assert "id" in data, "Response should contain field 'id'"
    assert "title" in data, "Response should contain field 'title'"
    assert "body" in data, "Response should contain field 'body'"


def test_get_post_by_id_has_expected_id(api_client):
    response = api_client.get_post(1)
    data = response.json()

    assert data["id"] == 1, f"Expected post id 1, got {data['id']}"


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post_by_id_parametrized(api_client, post_id):
    response = api_client.get_post(post_id)
    data = response.json()

    assert response.status_code == 200, (
        f"Expected status code 200 for post {post_id}, got {response.status_code}"
    )
    assert data["id"] == post_id, f"Expected post id {post_id}, got {data['id']}"


@pytest.mark.negative
def test_get_missing_post_returns_404(api_client):
    response = api_client.get_post(999999)

    assert response.status_code == 404, (
        f"Expected status code 404 for missing post, got {response.status_code}"
    )


@pytest.mark.negative
def test_get_missing_post_returns_empty_body(api_client):
    response = api_client.get_post(999999)
    data = response.json()

    assert data == {}, f"Expected empty response body, got {data}"


def test_get_posts_status_code(api_client):
    response = api_client.get_posts()

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )


def test_get_posts_returns_list(api_client):
    response = api_client.get_posts()
    data = response.json()

    assert isinstance(data, list), f"Expected list, got {type(data).__name__}"
    assert len(data) > 0, "Posts list should not be empty"


def test_get_posts_items_have_expected_fields(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert "userId" in post, f"Post should contain field 'userId': {post}"
        assert "id" in post, f"Post should contain field 'id': {post}"
        assert "title" in post, f"Post should contain field 'title': {post}"
        assert "body" in post, f"Post should contain field 'body': {post}"


def test_get_posts_items_have_expected_types(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert isinstance(post["userId"], int), f"userId should be int: {post}"
        assert isinstance(post["id"], int), f"id should be int: {post}"
        assert isinstance(post["title"], str), f"title should be str: {post}"
        assert isinstance(post["body"], str), f"body should be str: {post}"


def test_get_posts_response_time_is_within_timeout(api_client):
    response = api_client.get_posts()

    assert response.elapsed.total_seconds() < api_client.timeout, (
        f"Expected response time less than {api_client.timeout} seconds, "
        f"got {response.elapsed.total_seconds():.2f} seconds"
    )
