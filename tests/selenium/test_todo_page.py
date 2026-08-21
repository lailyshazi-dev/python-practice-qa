import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.selenium
def test_user_can_add_todo(selenium_driver, base_url):
    title = "Learn Selenium"

    selenium_driver.get(base_url)

    todo_input = WebDriverWait(selenium_driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "new-todo")
        )
    )
    todo_input.send_keys(title, Keys.ENTER)

    todo_item = WebDriverWait(selenium_driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".todo-list li")
        )
    )

    actual_title = todo_item.find_element(
        By.TAG_NAME,
        "label",
    ).text

    assert actual_title == title