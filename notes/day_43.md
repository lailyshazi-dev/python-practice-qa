# День 43: параметризация негативных тестов

## Что я сделал

- Создал ветку `refactor/parametrize-negative-calculator-tests`.
- Нашел два похожих негативных теста на деление на ноль.
- Объединил их в один параметризованный тест.
- Проверил только негативные calculator-тесты.
- Проверил весь проект.

## Что понял

- `@pytest.mark.parametrize` можно использовать не только для позитивных тестов.
- Если несколько негативных тестов отличаются только входными данными, их можно объединить.
- Один параметризованный тест запускается несколько раз: по одному разу для каждого набора данных.
- Количество проверок не уменьшается, уменьшается только дублирование кода.
- Код становится проще поддерживать: если меняется логика проверки, ее нужно изменить в одном месте.

## Где это нужно в реальной работе

- API должен вернуть ошибку для разных неправильных email: пустой email, email без `@`, слишком длинный email.
- Форма регистрации должна отклонять разные неправильные пароли.
- Backend должен одинаково обрабатывать разные запрещенные значения в payload.
- Финансовая система должна запрещать разные некорректные суммы: `0`, отрицательное число, слишком большое число.
- QA Automation Engineer не пишет 10 одинаковых тестов, а делает один понятный параметризованный тест.

## Было

```python
@pytest.mark.negative
def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


@pytest.mark.negative
def test_divide_negative_number_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(-10, 0)
```

## Стало

```python
@pytest.mark.negative
@pytest.mark.parametrize("number", [10, -10])
def test_divide_by_zero_raises_error(number):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(number, 0)
```

## Команды дня

```powershell
git switch -c refactor/parametrize-negative-calculator-tests
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py -m negative
.\.venv\Scripts\python.exe -m pytest
```

## Результат

```text
5 passed, 31 deselected
59 passed
```

## Новые слова

- `parametrize` - параметризовать, запускать один тест с разными данными.
- `test case` - отдельный тестовый случай.
- `input data` - входные данные.
- `duplication` - дублирование.
- `maintainability` - удобство поддержки кода.

## Правило дня

Если несколько тестов проверяют одно правило и отличаются только данными, подумай о параметризации.
