# День 20: pytest markers для API-тестов

## Что я сделал

- Создал ветку `feature/add-api-marker`.
- Добавил маркер `api` в `pytest.ini`.
- Пометил весь файл `tests/test_api_posts.py` как API-тесты.
- Запустил только API-тесты через `-m api`.
- Запустил все тесты проекта.
- Разобрал разницу между `selected` и `deselected`.

## Что понял

- Маркер позволяет объединять тесты в группы.
- Если весь файл содержит API-тесты, можно пометить весь файл одной строкой.
- `pytestmark = pytest.mark.api` применяет маркер `api` ко всем тестам файла.
- Команда `pytest -m api` запускает только тесты с маркером `api`.
- `deselected` означает, что pytest нашел тесты, но не выбрал их из-за фильтра.
- Остальные тесты не падают и не ломаются, они просто не запускаются в этом режиме.

## Код дня

```ini
[pytest]
markers =
    smoke: critical fast tests
    regression: full regression test set
    negative: tests for invalid input and errors
    api: API tests
```

```python
import pytest


pytestmark = pytest.mark.api
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
14 passed, 34 deselected
48 passed
```

## Новые слова

- `marker` - метка теста.
- `api marker` - метка для API-тестов.
- `selected` - тесты, выбранные для запуска.
- `deselected` - тесты, найденные, но не выбранные для запуска.
- `filter` - фильтр, который выбирает часть тестов.

## Правило дня

Маркер нужен, чтобы запускать не все тесты сразу, а только нужную группу.

