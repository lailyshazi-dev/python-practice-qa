# День 48: параметризация теста с pytest.approx

## Что я сделал

- Создал ветку `refactor/parametrize-approx-average-test`.
- Нашел одиночный тест с `pytest.approx`.
- Переделал его в параметризованный тест.
- Добавил три набора данных для проверки функции `average`.
- Добавил понятные `ids` для сценариев.
- Запустил параметризованный тест отдельно в подробном режиме.
- Запустил все тесты проекта.
- Проверил изменения через `git diff --check`.

## Что понял

- `pytest.approx` можно использовать внутри параметризованных тестов.
- Один тест может проверять несколько дробных расчетов.
- `ids` помогают понять, какой именно набор данных выполнился или упал.
- `abs=0.01` задает допустимую абсолютную погрешность.
- Параметризация уменьшает дублирование и делает тест проще расширять.

## Где это нужно в реальной работе

- Проверка среднего рейтинга товара на разных наборах оценок.
- Проверка среднего чека по разным заказам.
- Проверка среднего времени ответа API.
- Проверка среднего балла пользователя.
- Проверка расчетов процентов, коэффициентов и аналитических значений.
- Добавление новых расчетных сценариев без копирования одинакового теста.

Важно: `pytest.approx` не округляет результат, а разрешает небольшое отличие при сравнении.

## Было

```python
def test_average_returns_approx_result_with_tolerance():
    assert average(1, 2) == pytest.approx(1.5, abs=0.01)
```

## Стало

```python
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 1.5),
        (2, 5, 3.5),
        (1, 3, 2.0),
    ],
    ids=["average-1-and-2", "average-2-and-5", "average-1-and-3"],
)
def test_average_returns_approx_result_with_tolerance(a, b, expected):
    assert average(a, b) == pytest.approx(expected, abs=0.01)
```

## Команды дня

```powershell
git switch -c refactor/parametrize-approx-average-test
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_average_returns_approx_result_with_tolerance -vv
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
64 passed
git diff --check без ошибок
```

## Новые слова

- `calculation scenario` - расчетный сценарий.
- `average value` - среднее значение.
- `parameter set` - набор параметров.
- `approximate comparison` - приблизительное сравнение.
- `test expansion` - расширение теста новыми сценариями.

## Правило дня

Если одна формула должна работать на разных данных, параметризуй тест и используй `pytest.approx` для дробных результатов.
