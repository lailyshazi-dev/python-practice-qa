# День 52: функция failure_rate

## Что я сделал

- Создал ветку `feature/add-failure-rate-function`.
- Добавил функцию `failure_rate(failed, total)`.
- Внутри `failure_rate` переиспользовал функцию `percentage`.
- Добавил параметризованный тест для процента неуспешных операций.
- Добавил негативный тест для случая `total == 0`.
- Запустил новые тесты отдельно.
- Запустил все тесты проекта.
- Проверил изменения через `git diff --check`.

## Что понял

- `failure_rate` - это процент неуспешных операций от общего количества.
- Это такой же частный случай процента, как и `success_rate`.
- Если уже есть функция `percentage`, не нужно копировать формулу.
- Ошибка при `total == 0` переиспользуется из `percentage`.
- Парные функции `success_rate` и `failure_rate` удобно использовать для отчетов и мониторинга.

## Где это нужно в реальной работе

- В pytest-отчете можно считать процент упавших тестов.
- В CI/CD можно видеть процент failed jobs.
- В API-мониторинге можно считать процент ответов `4xx` и `5xx`.
- В платежной системе можно считать процент неуспешных оплат.
- В production dashboard можно отслеживать долю ошибок после релиза.

## Код дня

```python
def failure_rate(failed: int | float, total: int | float) -> float:
    return percentage(failed, total)
```

## Тесты дня

```python
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
```

```python
@pytest.mark.negative
def test_failure_rate_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        failure_rate(1, 0)
```

## Команды дня

```powershell
git switch -c feature/add-failure-rate-function
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_failure_rate_returns_expected_value -vv
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_failure_rate_with_zero_total_raises_error -vv
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
1 passed
76 passed
git diff --check без ошибок
```

## Новые слова

- `failure rate` - процент неуспешных операций.
- `failed` - неуспешные, упавшие, ошибочные операции.
- `monitoring` - наблюдение за состоянием системы.
- `error rate` - процент ошибок.
- `production dashboard` - панель метрик работающего продукта.

## Правило дня

Для метрик успеха и ошибок удобно делать отдельные понятные функции, но общую формулу лучше держать в одном месте.
