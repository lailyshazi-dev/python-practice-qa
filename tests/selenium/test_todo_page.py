import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

TODO_INPUT = (By.CLASS_NAME, "new-todo")
TODO_ITEM = (By.CSS_SELECTOR, ".todo-list li")
TODO_LABEL = (By.CSS_SELECTOR, ".todo-list li label")
TODO_COUNT = (By.CLASS_NAME, "todo-count")
TODO_TOGGLE = (By.CSS_SELECTOR, ".todo-list li .toggle")
CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")


def add_todo(wait, title):
    todo_input = wait.until(
        EC.visibility_of_element_located(TODO_INPUT),
        "Todo input did not appear",
    )
    todo_input.send_keys(title, Keys.ENTER)


@pytest.mark.selenium
def test_user_can_add_todo(selenium_driver, base_url, wait):
    title = "Learn Selenium"

    selenium_driver.get(base_url)
    add_todo(wait, title)

    todo_label = wait.until(
        EC.visibility_of_element_located(TODO_LABEL),
        "Todo did not appear in the list",
    )

    assert todo_label.text == title


@pytest.mark.selenium
def test_user_can_complete_and_clear_todo(selenium_driver, base_url, wait):
    title = "Learn explicit waits"

    selenium_driver.get(base_url)
    add_todo(wait, title)

    wait.until(
        EC.text_to_be_present_in_element(TODO_COUNT, "1 item left"),
        "Counter did not show '1 item left' after adding a todo",
    )

    # .toggle has opacity: 0, so is_displayed() is False and
    # element_to_be_clickable never succeeds. Wait for presence instead:
    # transparency does not block a WebDriver click.
    toggle = wait.until(
        EC.presence_of_element_located(TODO_TOGGLE),
        "Todo toggle did not appear in DOM",
    )
    toggle.click()

    wait.until(
        EC.text_to_be_present_in_element(TODO_COUNT, "0 items left"),
        "Counter did not reach '0 items left' after completing the todo",
    )

    clear_completed = wait.until(
        EC.element_to_be_clickable(CLEAR_COMPLETED),
        "Clear completed button did not become clickable",
    )
    clear_completed.click()

    wait.until(
        EC.invisibility_of_element_located(TODO_ITEM),
        "Todo is still visible after Clear completed",
    )

    assert selenium_driver.find_elements(*TODO_ITEM) == []
