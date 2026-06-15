# День 50: функция percentage и тесты для процентов

## Что я сделал

- Создал ветку `feature/add-percentage-function`.
- Добавил функцию `percentage(part, total)` в `src/calculator.py`.
- Добавил проверку ошибки, если `total` равен нулю.
- Добавил параметризованный позитивный тест для расчета процентов.
- Добавил негативный тест для деления на ноль внутри процентного расчета.
- Использовал `pytest.approx` для дробного процента.
- Проверил изменения через `git diff --check`.
- Запустил все тесты проекта.

## Что понял

- Процент считается по формуле `part / total * 100`.
- Если `total == 0`, процент посчитать нельзя, потому что будет деление на ноль.
- Для такой ситуации функция должна выбрасывать понятную ошибку.
- Позитивные тесты проверяют корректные расчеты.
- Негативный тест проверяет запрещенный случай.
- Для результата `1 / 3 * 100` удобно использовать `pytest.approx`, потому что получается дробное число `33.333333...`.

## Где это нужно в реальной работе

- В QA-отчете можно считать процент пройденных тестов: `passed / total * 100`.
- В интернет-магазине можно считать процент скидки или долю товаров определенной категории.
- В аналитике можно считать конверсию: количество покупок делится на количество посещений.
- В API-мониторинге можно считать процент успешных ответов: `2xx responses / all responses * 100`.
- В dashboard можно показывать процент выполнения задачи или прогресс загрузки.

## Код дня

```python
def percentage(part: int | float, total: int | float) -> float:
    if total == 0:
        raise ValueError("Cannot calculate percentage with zero total")

    return part / total * 100
```

## Тесты дня

```python
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
```

```python
@pytest.mark.negative
def test_percentage_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        percentage(10, 0)
```

## Команды дня

```powershell
git switch -c feature/add-percentage-function
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_percentage_returns_expected_value -vv
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_percentage_with_zero_total_raises_error -vv
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
1 passed
68 passed
git diff --check без ошибок
```

## Новые слова

- `percentage` - процент.
- `part` - часть от общего количества.
- `total` - общее количество.
- `conversion rate` - конверсия.
- `success rate` - процент успешных операций.

## Правило дня

Если функция делит на общее количество, обязательно проверь случай, когда общее количество равно нулю.
