import pytest

from src.calculator import (
    add,
    average,
    divide,
    factorial,
    is_even,
    list_average,
    list_sum,
    max_number,
    min_number,
    multiply,
    power,
    square,
    subtract,
    percentage,
    success_rate,
    failure_rate,
)


def test_divide_positive_numbers():
    assert divide(10, 2) == 5


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 3, 0.3333333333),
        (2, 3, 0.6666666667),
    ],
    ids=["one-divided-by-three", "two-divided-by-three"],
)
def test_divide_returns_approx_float_result(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(1, 2, 1.5, id="average-1-and-2"),
        pytest.param(2, 5, 3.5, id="average-2-and-5"),
        pytest.param(1, 3, 2.0, id="average-1-and-3"),
    ],
)
def test_average_returns_approx_result_with_tolerance(a, b, expected):
    assert average(a, b) == pytest.approx(expected, abs=0.01)


@pytest.mark.parametrize(
    "part, total, expected",
    [
        pytest.param(1, 2, 50.0, id="half"),
        pytest.param(3, 4, 75.0, id="three-quarters"),
        pytest.param(1, 3, 33.3333333333, id="one-third"),
    ],
)
def test_percentage_returns_expected_value(part, total, expected):
    assert percentage(part, total) == pytest.approx(expected, abs=0.01)


@pytest.mark.negative
def test_percentage_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        percentage(10, 0)


def test_power():
    assert power(2, 3) == 8


def test_power_with_zero_exponent():
    assert power(5, 0) == 1


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


def test_list_sum(sample_numbers):
    assert list_sum(sample_numbers) == 15


def test_list_average(sample_numbers):
    assert list_average(sample_numbers) == 3


def test_calculator_config(calculator_config):
    assert calculator_config["precision"] == 2
    assert calculator_config["mode"] == "standard"


@pytest.mark.smoke
def test_add_positive_numbers():
    assert add(2, 3) == 5


@pytest.mark.smoke
def test_subtract_positive_numbers():
    assert subtract(10, 4) == 6


@pytest.mark.smoke
def test_multiply_positive_numbers():
    assert multiply(6, 7) == 42


@pytest.mark.negative
@pytest.mark.parametrize("number", [10, -10])
def test_divide_by_zero_raises_error(number):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(number, 0)
        

@pytest.mark.negative
def test_factorial_with_negative_number_raises_error():
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial(-1)


@pytest.mark.negative
@pytest.mark.parametrize(
    "numbers, expected_error",
    [
        ([], "Cannot calculate average of empty list"),
        (list(), "Cannot calculate average of empty list"),
    ],
    ids=["empty-list-literal", "empty-list-constructor"],
)
def test_list_average_with_empty_list_raises_error(numbers, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        list_average(numbers)
        
        
@pytest.mark.regression
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
    "successful, total, expected",
    [
        pytest.param(8, 10, 80.0, id="eight-of-ten"),
        pytest.param(64, 68, 94.1176470588, id="sixty-four-of-sixty-eight"),
        pytest.param(0, 10, 0.0, id="zero-successful"),
    ],
)
def test_success_rate_returns_expected_value(successful, total, expected):
    assert success_rate(successful, total) == pytest.approx(expected, abs=0.01)


@pytest.mark.negative
def test_success_rate_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        success_rate(10, 0)


@pytest.mark.parametrize(
    "failed, total, expected",
    [
        pytest.param(2, 10, 20.0, id="two-of-ten"),
        pytest.param(4, 68, 5.8823529412, id="four-of-sixty-eight"),
        pytest.param(0, 10, 0.0, id="zero-failed"),
    ],
)
def test_failure_rate_returns_expected_value(failed, total, expected):
    assert failure_rate(failed, total) == pytest.approx(expected, abs=0.01)


@pytest.mark.negative
def test_failure_rate_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        failure_rate(1, 0)
