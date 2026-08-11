import pytest
from playwright.sync_api import Page

from tests.ui.pages.todo_page import TodoPage


@pytest.fixture
def todo_page(page: Page, base_url: str) -> TodoPage:
    page.goto(base_url)

    return TodoPage(page)