from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class SeleniumTodoPage:
    TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_ITEM = (By.CSS_SELECTOR, ".todo-list li")
    TODO_LABEL = (By.CSS_SELECTOR, ".todo-list li label")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    TODO_TOGGLE = (By.CSS_SELECTOR, ".todo-list li .toggle")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, url):
        self.driver.get(url)

    def add_todo(self, title):
        todo_input = self.wait.until(
            EC.visibility_of_element_located(self.TODO_INPUT),
            "Todo input did not appear",
        )
        todo_input.send_keys(title, Keys.ENTER)

    def first_todo_title(self):
        label = self.wait.until(
            EC.visibility_of_element_located(self.TODO_LABEL),
            "Todo did not appear in the list",
        )
        return label.text

    def complete_first_todo(self):
        # .toggle has opacity: 0, so is_displayed() is False and
        # element_to_be_clickable never succeeds. Wait for presence instead:
        # transparency does not block a WebDriver click.
        toggle = self.wait.until(
            EC.presence_of_element_located(self.TODO_TOGGLE),
            "Todo toggle did not appear in DOM",
        )
        toggle.click()

    def clear_completed(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.CLEAR_COMPLETED),
            "Clear completed button did not become clickable",
        )
        button.click()

    def wait_items_left(self, text):
        self.wait.until(
            EC.text_to_be_present_in_element(self.TODO_COUNT, text),
            f"Counter did not show '{text}'",
        )

    def wait_list_empty(self):
        self.wait.until(
            EC.invisibility_of_element_located(self.TODO_ITEM),
            "Todo is still visible after Clear completed",
        )

    def visible_todos(self):
        return self.driver.find_elements(*self.TODO_ITEM)
