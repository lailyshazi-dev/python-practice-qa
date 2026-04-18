import pytest


@pytest.fixture(scope="function")
def sample_numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture(scope="module")
def calculator_config():
    return {
        "precision": 2,
        "mode": "standard",
    }
