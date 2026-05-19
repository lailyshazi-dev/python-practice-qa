# Python Practice QA

Учебный репозиторий для восстановления Python и подготовки к QA Automation.

## Цели проекта

- повторить базовый Python;
- научиться писать понятные функции;
- покрывать функции тестами на pytest;
- привыкнуть к структуре проекта и Git.

## Структура

```text
src/      код на Python
tests/    автотесты
notes/    короткие конспекты
```


## Как запустить тесты

Проект настроен через `pytest.ini`: pytest автоматически ищет тесты в папке `tests` и использует короткий вывод.

Запуск всех тестов:

```powershell
python -m pytest
```

Запуск только API-тестов по папке:

```powershell
python -m pytest tests/api
```

Запуск только API-тестов по маркеру:

```powershell
python -m pytest -m api
```

Запуск негативных API-тестов:

```powershell
python -m pytest -m "api and negative"
```

Запуск API-тестов без негативных сценариев:

```powershell
python -m pytest -m "api and not negative"
```

Генерация HTML-отчета:

```powershell
python -m pytest --html=reports/report.html --self-contained-html
```


