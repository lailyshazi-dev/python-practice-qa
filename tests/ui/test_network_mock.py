import pytest
from playwright.sync_api import Page, Route


pytestmark = pytest.mark.ui


def test_browser_can_use_mocked_api_response(
    page: Page,
):
    def fulfill_status(route: Route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"status": "ok", "source": "mock"}',
        )

    page.route(
        "**/api/status",
        fulfill_status,
    )
    page.goto("https://example.com")

    result = page.evaluate(
        """
        async () => {
            const response = await fetch("/api/status");

            return {
                status: response.status,
                body: await response.json(),
            };
        }
        """
    )

    assert result == {
        "status": 200,
        "body": {
            "status": "ok",
            "source": "mock",
        },
    }