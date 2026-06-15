# День 51: функция success_rate и переиспользование кода

## Что я сделал

- Создал ветку `feature/add-success-rate-function`.
- Добавил функцию `success_rate(successful, total)`.
- Внутри `success_rate` переиспользовал уже готовую функцию `percentage`.
- Добавил параметризованный тест для расчета процента успешных операций.
- Добавил негативный тест для случая `total == 0`.
- Запустил новые тесты отдельно.
- Запустил все тесты проекта.
- Проверил изменения через `git diff --check`.

## Что понял

- Не всегда нужно писать формулу заново.
- Если уже есть универсальная функция, ее можно переиспользовать в более конкретной функции.
- `success_rate` - это частный случай процента: успешные операции делятся на общее количество.
- Ошибка при `total == 0` приходит из функции `percentage`, потому что `success_rate` вызывает ее внутри.
- Переиспользование кода уменьшает дублирование и риск ошибок.

## Где это нужно в реальной работе

- В тестовом отчете можно считать процент пройденных тестов: `passed / total * 100`.
- В API-мониторинге можно считать процент успешных ответов: `2xx responses / all responses * 100`.
- В CI/CD можно показывать success rate сборок или автотестов.
- В продуктовой аналитике можно считать процент успешных оплат, регистраций или доставок.
- В dashboard можно отображать качество релиза: сколько проверок прошло успешно из общего количества.

## Код дня

```python
def success_rate(successful: int | float, total: int | float) -> float:
    return percentage(successful, total)
```

## Тесты дня

```python
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
```

```python
@pytest.mark.negative
def test_success_rate_with_zero_total_raises_error():
    with pytest.raises(ValueError, match="Cannot calculate percentage with zero total"):
        success_rate(10, 0)
```

## Команды дня

```powershell
git switch -c feature/add-success-rate-function
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_success_rate_returns_expected_value -vv
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_success_rate_with_zero_total_raises_error -vv
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
1 passed
72 passed
git diff --check без ошибок
```

## Новые слова

- `success rate` - процент успешных операций.
- `reuse` - переиспользование.
- `duplication` - дублирование.
- `wrapper function` - функция-обертка, которая использует другую функцию.
- `dashboard metric` - метрика для отчета или панели мониторинга.

## Правило дня

Если новая функция является частным случаем уже существующей логики, лучше переиспользовать готовую функцию, а не копировать формулу.
