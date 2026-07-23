import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.ui

EXAMPLE_URL = "https://example.com"


def test_example_page_has_expected_title(page: Page):
    page.goto(EXAMPLE_URL)

    expect(page).to_have_title("Example Domain")


def test_example_page_has_visible_heading(page: Page):
    page.goto(EXAMPLE_URL)

    heading = page.get_by_role(
        "heading",
        name="Example Domain",
    )

    expect(heading).to_be_visible()
