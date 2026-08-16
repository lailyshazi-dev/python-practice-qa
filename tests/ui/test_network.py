import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_todomvc_initial_document_returns_ok(
    page: Page,
    base_url: str,
):
    with page.expect_response(
        lambda response: (
            response.url == base_url
            and response.request.method == "GET"
        )
    ) as response_info:
        page.goto(base_url)

    response = response_info.value

    assert response.ok
    assert response.status == 200
    expect(page).to_have_url(
        f"{base_url}#/"
    )
