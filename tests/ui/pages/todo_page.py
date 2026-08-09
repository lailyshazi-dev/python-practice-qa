from playwright.sync_api import Locator, Page


class TodoPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.todo_input = page.get_by_placeholder(
            "What needs to be done?"
        )
        self.todo_items = page.get_by_test_id("todo-item")
        self.todo_toggle = page.get_by_role(
            "checkbox",
            name="Toggle Todo",
        )

    def add_todo(self, title: str) -> None:
        self.todo_input.fill(title)
        self.todo_input.press("Enter")

    def complete_todo(self) -> None:
        self.todo_toggle.check()

    def todo_title(self, title: str) -> Locator:
        return self.page.get_by_text(
            title,
            exact=True,
        )

    def items_left(self, count: int) -> Locator:
        word = "item" if count == 1 else "items"

        return self.page.get_by_text(
            f"{count} {word} left",
            exact=True,
        )
