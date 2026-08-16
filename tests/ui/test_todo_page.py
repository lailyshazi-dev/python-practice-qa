import pytest
from playwright.sync_api import expect

from tests.ui.pages.todo_page import TodoPage


pytestmark = pytest.mark.ui


@pytest.mark.parametrize(
    "title",
    [
        "Learn Playwright locators",
        "Practice UI assertions",
    ],
    ids=[
        "locators",
        "assertions",
    ],
)
@pytest.mark.smoke
def test_user_can_add_todo(
    todo_page: TodoPage,
    title: str,
):
    todo_page.add_todo(title)

    expect(
        todo_page.todo_title(title)
    ).to_be_visible()
    expect(todo_page.todo_items).to_have_count(1)
    expect(todo_page.items_left(1)).to_be_visible()


def test_user_can_complete_todo(todo_page: TodoPage):
    title = "Complete Playwright lesson"
    todo_page.add_todo(title)
    todo_page.complete_todo(title)
    todo_item = todo_page.todo_item(title)

    expect(
        todo_item.get_by_role(
            "checkbox",
            name="Toggle Todo",
        )
    ).to_be_checked()
    expect(todo_page.items_left(0)).to_be_visible()


def test_new_browser_context_has_empty_todo_list(
    todo_page: TodoPage,
):
    expect(todo_page.todo_items).to_have_count(0)


def test_user_can_filter_completed_todos(
    todo_page: TodoPage,
):
    active_title = "Keep active"
    completed_title = "Complete this"

    todo_page.add_todo(active_title)
    todo_page.add_todo(completed_title)
    todo_page.complete_todo(completed_title)
    todo_page.show_completed()

    expect(
        todo_page.todo_item(completed_title)
    ).to_be_visible()
    expect(
        todo_page.todo_item(active_title)
    ).to_be_hidden()


@pytest.mark.parametrize(
    "title, expected_count",
    [
        pytest.param(
            "Buy milk",
            1,
            id="valid-title",
        ),
        pytest.param(
            "",
            0,
            id="empty-title",
        ),
    ],
)
def test_add_todo_result(
    todo_page: TodoPage,
    title: str,
    expected_count: int,
):
    todo_page.add_todo(title)

    expect(todo_page.todo_items).to_have_count(
        expected_count
    )
