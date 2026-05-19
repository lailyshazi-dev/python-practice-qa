# День 36: testpaths в pytest.ini

## Что я сделал

- Создал ветку `config/add-pytest-testpaths`.
- Добавил `testpaths = tests` в `pytest.ini`.
- Запустил все тесты обычной командой.
- Запустил API-тесты по маркеру.
- Проверил, что настройка не сломала запуск тестов.

## Что понял

- `testpaths` указывает pytest, где искать тесты.
- В нашем проекте тесты лежат в папке `tests`.
- Теперь pytest явно знает, что искать тесты нужно именно там.
- Это делает запуск более предсказуемым.
- `testpaths` не меняет сами тесты, а настраивает поиск тестов.

## Где это нужно в реальной работе

- В большом проекте рядом могут быть папки `src`, `docs`, `scripts`, `tools`, `reports`.
- Без настройки pytest может искать тесты шире, чем нужно.
- В монорепозитории может быть несколько разных тестовых папок.
- Команде проще понимать проект, когда в `pytest.ini` явно указано, где лежат тесты.
- В CI настройка `testpaths` помогает запускать именно нужный набор тестов.

## Код дня

```ini
[pytest]
addopts = -q
testpaths = tests
markers =
    smoke: critical fast tests
    regression: full regression test set
    negative: tests for invalid input and errors
    api: API tests
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pytest -m api
```

## Результат

```text
57 passed
23 passed, 34 deselected
```

## Новые слова

- `testpaths` - настройка путей, где pytest ищет тесты.
- `path` - путь к папке или файлу.
- `discovery` - поиск тестов.
- `predictable` - предсказуемый.
- `monorepo` - большой репозиторий с несколькими проектами внутри.

## Правило дня

Если все тесты проекта лежат в одной папке, лучше явно указать ее в `pytest.ini` через `testpaths`.

