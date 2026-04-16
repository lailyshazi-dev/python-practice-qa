def add(a: int | float, b: int | float) -> int | float:
    return a + b


def subtract(a: int | float, b: int | float) -> int | float:
    return a - b


def multiply(a: int | float, b: int | float) -> int | float:
    return a * b


def divide(a: int | float, b: int | float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


def power(a: int | float, b: int | float) -> int | float:
    return a ** b


def is_even(number: int) -> bool:
    return number % 2 == 0


def max_number(a: int | float, b: int | float) -> int | float:
    return max(a, b)


def min_number(a: int | float, b: int | float) -> int | float:
    return min(a, b)


def square(number: int | float) -> int | float:
    return number * number


def average(a: int | float, b: int | float) -> float:
    return (a + b) / 2


def factorial(number: int) -> int:
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers")

    result = 1

    for value in range(1, number + 1):
        result = result * value

    return result
