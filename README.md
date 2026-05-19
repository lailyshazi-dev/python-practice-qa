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

Запуск всех тестов:

```powershell
python -m pytest
```

Короткий запуск всех тестов:

```powershell
python -m pytest -q
```

Запуск только API-тестов по папке:

```powershell
python -m pytest tests/api -q
```

Запуск только API-тестов по маркеру:

```powershell
python -m pytest -m api -q
```

Запуск негативных API-тестов:

```powershell
python -m pytest -m "api and negative" -q
```

Запуск API-тестов без негативных сценариев:

```powershell
python -m pytest -m "api and not negative" -q
```

Генерация HTML-отчета:

```powershell
python -m pytest --html=reports/report.html --self-contained-html
```


