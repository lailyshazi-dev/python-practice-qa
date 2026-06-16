# День 53: test run summary и правило именования функций

## Что я сделал

- Создал ветку `feature/add-test-run-summary`.
- Добавил функцию `calculate_test_run_summary(passed, failed)`.
- Функция возвращает словарь со сводкой тестового прогона.
- Добавил параметризованный тест для разных результатов прогона.
- Добавил негативный тест для случая, когда всего тестов `0`.
- Разобрал ошибку pytest collection из-за имени функции `test_run_summary`.
- Запустил все тесты проекта.
- Проверил изменения через `git diff --check`.

## Что понял

- Pytest считает тестами функции, которые начинаются с `test_`.
- Если импортировать обычную функцию с именем `test_run_summary` в тестовый файл, pytest может принять ее за тест.
- Тогда параметры обычной функции pytest попытается найти как fixtures.
- Поэтому production-функции лучше не называть с префиксом `test_`.
- Для обычной функции лучше использовать имя вроде `calculate_test_run_summary`.

## Где это нужно в реальной работе

- В проектах с pytest важно соблюдать соглашения об именовании.
- Тестовые функции называют `test_...`, а обычные helper/business функции не должны выглядеть как тесты.
- Если случайно импортировать helper с именем `test_...`, можно получить странную ошибку про missing fixture.
- В CI/CD такая ошибка может сломать весь pipeline, хотя бизнес-логика написана правильно.
- Отчеты по автотестам часто строят summary: сколько прошло, сколько упало, какой success rate и failure rate.

## Ошибка дня

Сначала функция называлась так:

```python
def test_run_summary(passed: int, failed: int) -> dict[str, int | float]:
```

Pytest увидел имя `test_run_summary` и решил, что это тест. После этого он попытался найти fixtures `passed` и `failed`.

Ошибка была примерно такая:

```text
fixture 'passed' not found
```

Правильное имя:

```python
def calculate_test_run_summary(passed: int, failed: int) -> dict[str, int | float]:
```

## Код дня

```python
def calculate_test_run_summary(passed: int, failed: int) -> dict[str, int | float]:
    total = passed + failed

    if total == 0:
        raise ValueError("Cannot calculate test run summary with zero total")

    return {
        "total": total,
        "success_rate": success_rate(passed, total),
        "failure_rate": failure_rate(failed, total),
    }
```

## Тесты дня

```python
@pytest.mark.parametrize(
    "passed, failed, expected_total, expected_success_rate, expected_failure_rate",
    [
        pytest.param(8, 2, 10, 80.0, 20.0, id="mostly-passed"),
        pytest.param(64, 4, 68, 94.1176470588, 5.8823529412, id="real-project-example"),
        pytest.param(0, 10, 10, 0.0, 100.0, id="all-failed"),
    ],
)
def test_test_run_summary_returns_expected_data(
    passed,
    failed,
    expected_total,
    expected_success_rate,
    expected_failure_rate,
):
    summary = calculate_test_run_summary(passed, failed)

    assert summary["total"] == expected_total
    assert summary["success_rate"] == pytest.approx(expected_success_rate, abs=0.01)
    assert summary["failure_rate"] == pytest.approx(expected_failure_rate, abs=0.01)
```

```python
@pytest.mark.negative
def test_test_run_summary_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate test run summary with zero total"):
        calculate_test_run_summary(0, 0)
```

## Команды дня

```powershell
git switch -c feature/add-test-run-summary
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_test_run_summary_returns_expected_data -vv
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_test_run_summary_with_zero_total_raises_error -vv
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
1 passed
80 passed
git diff --check без ошибок
```

## Новые слова

- `test collection` - этап, когда pytest ищет тесты.
- `fixture not found` - ошибка, когда pytest не нашел fixture с нужным именем.
- `summary` - сводка.
- `naming convention` - соглашение об именовании.
- `business function` - обычная функция приложения, не тест.

## Правило дня

Не называй обычные функции с префиксом `test_`, если они могут быть импортированы в тестовый файл: pytest может принять их за тесты.
