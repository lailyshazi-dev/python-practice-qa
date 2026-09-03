import os

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.selenium.pages.todo_page import SeleniumTodoPage

EXPLICIT_TIMEOUT = 10


@pytest.fixture
def selenium_driver():
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)

    yield driver

    driver.quit()


@pytest.fixture
def wait(selenium_driver):
    return WebDriverWait(selenium_driver, EXPLICIT_TIMEOUT)


@pytest.fixture
def todo_page(selenium_driver, wait):
    return SeleniumTodoPage(selenium_driver, wait)
