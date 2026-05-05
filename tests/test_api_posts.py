import pytest


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

def test_get_missing_post_returns_404(api_client):
    response = api_client.get_post(999999)

    assert response.status_code == 404


def test_get_missing_post_returns_empty_body(api_client):
    response = api_client.get_post(999999)
    data = response.json()

    assert data == {}
