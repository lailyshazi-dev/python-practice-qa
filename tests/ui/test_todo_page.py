import pytest
from playwright.sync_api import expect

from tests.ui.pages.todo_page import TodoPage


pytestmark = pytest.mark.ui


def test_user_can_add_todo(todo_page: TodoPage):
    todo_page.add_todo("Learn Playwright locators")

    expect(
        todo_page.todo_title(
            "Learn Playwright locators"
        )
    ).to_be_visible()
    expect(todo_page.todo_items).to_have_count(1)
    expect(todo_page.items_left(1)).to_be_visible()


def test_user_can_complete_todo(todo_page: TodoPage):
    todo_page.add_todo("Complete Playwright lesson")
    todo_page.complete_todo()

    expect(todo_page.todo_toggle).to_be_checked()
    expect(todo_page.items_left(0)).to_be_visible()


def test_new_browser_context_has_empty_todo_list(
    todo_page: TodoPage,
):
    expect(todo_page.todo_items).to_have_count(0)
