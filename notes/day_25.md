# День 25: вынос API-клиента в отдельный файл

## Что я сделал

- Создал ветку `refactor/move-api-client-to-src`.
- Создал файл `src/api_client.py`.
- Перенес класс `ApiClient` из `tests/conftest.py` в `src/api_client.py`.
- Обновил импорт `ApiClient` в `tests/conftest.py`.
- Оставил в `conftest.py` только фикстуры.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `src/` хранит код проекта.
- `tests/` хранит тесты и тестовую настройку.
- `conftest.py` лучше использовать для фикстур, а не для основной логики клиента.
- Вынос класса в отдельный файл делает структуру проекта понятнее.
- Такой рефакторинг не должен менять поведение тестов.
- Если после рефакторинга тесты проходят, значит перенос выполнен правильно.

## Код дня

```python
from src.api_client import ApiClient
```

```python
@pytest.fixture(scope="module")
def api_client():
    return ApiClient("https://jsonplaceholder.typicode.com")
```

## Новая структура

```text
src/
  api_client.py
  calculator.py

tests/
  conftest.py
  test_api_posts.py
  test_calculator.py
```

## Команды дня

```powershell
git switch -c refactor/move-api-client-to-src
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
15 passed, 34 deselected
49 passed
```

## Новые слова

- `project code` - код проекта.
- `test code` - код тестов.
- `separation` - разделение.
- `import` - подключение кода из другого файла.
- `module` - Python-файл, который можно импортировать.

## Правило дня

Код, который тестируется или используется как часть проекта, лучше хранить в `src/`, а тестовые фикстуры - в `tests/conftest.py`.

