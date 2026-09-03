import pytest

pytestmark = pytest.mark.selenium


def test_user_can_add_todo(todo_page, base_url):
    title = "Learn Selenium"

    todo_page.open(base_url)
    todo_page.add_todo(title)

    assert todo_page.first_todo_title() == title


def test_user_can_complete_and_clear_todo(todo_page, base_url):
    title = "Learn explicit waits"

    todo_page.open(base_url)
    todo_page.add_todo(title)
    todo_page.wait_items_left("1 item left")

    todo_page.complete_first_todo()
    todo_page.wait_items_left("0 items left")

    todo_page.clear_completed()
    todo_page.wait_list_empty()

    assert todo_page.visible_todos() == []
