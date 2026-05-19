# День 35: настройка pytest.ini для стандартного запуска

## Что я сделал

- Создал ветку `config/add-pytest-default-options`.
- Добавил `addopts = -q` в `pytest.ini`.
- Запустил все тесты без явного `-q`.
- Запустил API-тесты по маркеру без явного `-q`.
- Проверил, что pytest теперь использует короткий вывод по умолчанию.

## Что понял

- `pytest.ini` хранит настройки pytest для проекта.
- `addopts` задает параметры, которые pytest применяет при каждом запуске.
- `addopts = -q` делает вывод короче по умолчанию.
- Теперь можно писать `python -m pytest`, а pytest будет запускаться как `python -m pytest -q`.
- Это помогает сделать запуск тестов одинаковым для всей команды.

## Где это нужно в реальной работе

- В команде все QA и разработчики запускают тесты с одинаковыми настройками.
- В CI можно использовать простую команду `python -m pytest`, а нужные флаги уже будут в конфиге.
- Новому человеку не нужно помнить все флаги запуска.
- Если команда решит добавить стандартный отчет или строгие предупреждения, это можно будет сделать в одном месте.

## Код дня

```ini
[pytest]
addopts = -q
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

- `addopts` - стандартные параметры запуска pytest.
- `default option` - параметр по умолчанию.
- `configuration` - настройка.
- `standard run` - стандартный запуск.
- `consistent` - одинаковый, согласованный.

## Правило дня

Если команда всегда запускает pytest с одними и теми же флагами, эти флаги лучше перенести в `pytest.ini`.

