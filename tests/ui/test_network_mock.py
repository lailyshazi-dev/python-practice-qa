import json

import pytest
from playwright.sync_api import Page, Route


pytestmark = pytest.mark.ui

@pytest.mark.parametrize(
    "status_code, payload, expected_ok",
    [
        pytest.param(
            200,
            {
                "status": "ok",
                "source": "mock",
            },
            True,
            id="success-response",
        ),
        pytest.param(
            500,
            {
                "error": "Internal Server Error",
            },
            False,
            id="server-error",
        ),
        pytest.param(
            200,
            {
                "items": [],
            },
            True,
            id="empty-list",
        ),
    ],
)

def test_browser_can_use_mocked_api_response(
    page: Page,
    status_code: int,
    payload: dict,
    expected_ok: bool,
):
    def fulfill_status(route: Route):
        route.fulfill(
            status=status_code,
            content_type="application/json",
            body=json.dumps(payload),
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
                ok: response.ok,
                status: response.status,
                body: await response.json(),
            };
        }
        """
    )

    assert result == {
        "ok": expected_ok,
        "status": status_code,
        "body": payload,
    }
