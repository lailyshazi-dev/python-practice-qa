import os

import pytest
from selenium import webdriver


@pytest.fixture
def selenium_driver():
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)

    yield driver

    driver.quit()
