from playwright.sync_api import Locator, Page


class TodoPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.todo_input = page.get_by_placeholder(
            "What needs to be done?"
        )
        self.todo_items = page.get_by_test_id("todo-item")

    def add_todo(self, title: str) -> None:
        self.todo_input.fill(title)
        self.todo_input.press("Enter")

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

    def todo_item(self, title: str) -> Locator:
        return self.todo_items.filter(has_text=title)

    def show_completed(self) -> None:
        self.page.get_by_role(
            "link",
            name="Completed",
        ).click()

    def complete_todo(self, title: str) -> None:
        todo_item = self.todo_item(title)

        todo_item.get_by_role(
            "checkbox",
            name="Toggle Todo",
        ).check()