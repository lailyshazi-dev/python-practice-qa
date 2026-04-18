import pytest

from src.calculator import add, divide, is_even, max_number, min_number, multiply, power, subtract, square, average, factorial, list_sum, list_average


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


def test_square():
    assert square(5) == 25


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 4, 3),
        (10, 20, 15),
        (-2, 2, 0),
        (1.5, 2.5, 2),
    ],
)
def test_average(a, b, expected):
    assert average(a, b) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (0, 1),
        (1, 1),
        (3, 6),
        (5, 120),
    ],
)
def test_factorial(number, expected):
    assert factorial(number) == expected


def test_factorial_with_negative_number_raises_error():
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial(-1)


def test_list_sum(sample_numbers):
    assert list_sum(sample_numbers) == 15


def test_list_average(sample_numbers):
    assert list_average(sample_numbers) == 3


def test_list_average_with_empty_list_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
        list_average([])


def test_calculator_config(calculator_config):
    assert calculator_config["precision"] == 2
    assert calculator_config["mode"] == "standard"
