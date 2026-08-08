import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.ui


def test_user_can_add_todo(todo_page: Page):
    todo_input = todo_page.get_by_placeholder(
        "What needs to be done?"
    )

    todo_input.fill("Learn Playwright locators")
    todo_input.press("Enter")

    expect(
        todo_page.get_by_text(
            "Learn Playwright locators",
            exact=True,
        )
    ).to_be_visible()
    expect(todo_page.get_by_test_id("todo-item")).to_have_count(1)
    expect(
        todo_page.get_by_text("1 item left", exact=True)
    ).to_be_visible()


def test_user_can_complete_todo(todo_page: Page):
    todo_input = todo_page.get_by_placeholder(
        "What needs to be done?"
    )
    todo_input.fill("Complete Playwright lesson")
    todo_input.press("Enter")

    toggle = todo_page.get_by_role(
        "checkbox",
        name="Toggle Todo",
    )
    toggle.check()

    expect(toggle).to_be_checked()
    expect(
        todo_page.get_by_text("0 items left", exact=True)
    ).to_be_visible()


def test_new_browser_context_has_empty_todo_list(todo_page: Page):
    expect(todo_page.get_by_test_id("todo-item")).to_have_count(0)
