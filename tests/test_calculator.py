import pytest

from src.calculator import add, divide, is_even, max_number, min_number, multiply, power, subtract


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_subtract_positive_numbers():
    assert subtract(10, 4) == 6


def test_multiply_positive_numbers():
    assert multiply(6, 7) == 42


def test_divide_positive_numbers():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_power():
    assert power(2, 3) == 8


def test_power_with_zero_exponent():
    assert power(5, 0) == 1


@pytest.mark.parametrize(
    "number, expected",
    [
        (4, True),
        (5, False),
        (0, True),
        (-2, True),
        (-3, False),
    ],
)
def test_is_even(number, expected):
    assert is_even(number) is expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 10),
        (2, 9, 9),
        (-1, -5, -1),
        (4, 4, 4),
    ],
)
def test_max_number(a, b, expected):
    assert max_number(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 3),
        (2, 9, 2),
        (-1, -5, -5),
        (4, 4, 4),
    ],
)
def test_min_number(a, b, expected):
    assert min_number(a, b) == expected
