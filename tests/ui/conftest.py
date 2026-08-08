import pytest
from playwright.sync_api import Page


@pytest.fixture
def todo_page(page: Page, base_url: str):
    page.goto(base_url)

    return page