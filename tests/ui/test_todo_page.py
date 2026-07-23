import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.ui

TODO_URL = "https://demo.playwright.dev/todomvc/"


def test_user_can_add_todo(page: Page):
    page.goto(TODO_URL)

    todo_input = page.get_by_placeholder(
        "What needs to be done?"
    )

    todo_input.fill("Learn Playwright locators")
    todo_input.press("Enter")

    expect(
        page.get_by_text(
            "Learn Playwright locators",
            exact=True,
        )
    ).to_be_visible()
    expect(page.get_by_test_id("todo-item")).to_have_count(1)
    expect(
        page.get_by_text("1 item left", exact=True)
    ).to_be_visible()


def test_user_can_complete_todo(page: Page):
    page.goto(TODO_URL)

    todo_input = page.get_by_placeholder(
        "What needs to be done?"
    )
    todo_input.fill("Complete Playwright lesson")
    todo_input.press("Enter")

    toggle = page.get_by_role(
        "checkbox",
        name="Toggle Todo",
    )
    toggle.check()

    expect(toggle).to_be_checked()
    expect(
        page.get_by_text("0 items left", exact=True)
    ).to_be_visible()


def test_new_browser_context_has_empty_todo_list(page: Page):
    page.goto(TODO_URL)

    expect(page.get_by_test_id("todo-item")).to_have_count(0)
