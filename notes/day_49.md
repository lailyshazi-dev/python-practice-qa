# День 49: pytest.param для читаемой параметризации

## Что я сделал

- Создал ветку `refactor/use-pytest-param-for-average-test`.
- Переделал параметризацию теста `average` на `pytest.param`.
- Перенес `id` каждого сценария ближе к его данным.
- Запустил параметризованный тест отдельно в подробном режиме.
- Запустил все тесты проекта.
- Проверил изменения через `git diff --check`.

## Что понял

- `pytest.param` позволяет описывать один набор параметров явно.
- В `pytest.param` можно указать `id` прямо рядом с данными.
- Так меньше риск перепутать данные и имя сценария.
- Такой формат удобнее читать, когда параметров становится много.
- Логика теста не изменилась: изменился только способ записи параметров.

## Где это нужно в реальной работе

- API-тесты: каждый payload можно подписать рядом с данными, например `missing-title`, `empty-body`, `invalid-user-id`.
- UI-тесты: сценарии формы можно назвать `empty-email`, `invalid-password`, `blocked-user`.
- Негативные тесты: разные ошибки можно хранить как отдельные `pytest.param`.
- Большие таблицы тестовых данных легче поддерживать, когда `id` находится рядом со своим набором параметров.
- В CI/CD и HTML-отчетах по `id` сразу видно, какой сценарий упал.

## Было

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

## Стало

```python
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
```

## Команды дня

```powershell
git switch -c refactor/use-pytest-param-for-average-test
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

- `pytest.param` - явное описание одного набора параметров.
- `id` - имя сценария в выводе pytest.
- `payload case` - сценарий с конкретным набором данных для API.
- `readability` - читаемость.
- `data-driven test` - тест, который управляется наборами данных.

## Правило дня

Если у параметризованного теста есть важные имена сценариев, удобно хранить данные и `id` вместе через `pytest.param`.
