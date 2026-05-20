# День 38: отдельный conftest.py для API-тестов

## Что я сделал

- Создал ветку `refactor/move-api-fixtures-to-api-conftest`.
- Создал файл `tests/api/conftest.py`.
- Перенес API-фикстуры ближе к API-тестам.
- Оставил в `tests/conftest.py` только общие фикстуры для калькулятора.
- Проверил, что API-тесты видят фикстуры из `tests/api/conftest.py`.
- Запустил API-тесты.
- Запустил все тесты проекта.

## Что понял

- `conftest.py` может быть не только один на весь проект.
- `tests/conftest.py` доступен всем тестам внутри папки `tests`.
- `tests/api/conftest.py` доступен тестам внутри папки `tests/api`.
- Фикстуры лучше держать ближе к тем тестам, которым они нужны.
- Так общий `conftest.py` не превращается в большой файл со всем подряд.

## Где это нужно в реальной работе

- API-тестам нужны API-клиент, токены, payload и базовые данные.
- UI-тестам нужны браузер, страница, авторизация и Page Object.
- DB-тестам нужно подключение к базе и подготовка данных.
- Если все эти фикстуры положить в один общий `conftest.py`, файл станет сложным и неудобным.
- В рабочем проекте локальные `conftest.py` помогают разделять тестовую инфраструктуру по слоям: API, UI, DB, integration.

## Новая структура

```text
tests/
  conftest.py
  api/
    conftest.py
    test_create_post.py
    test_delete_post.py
    test_get_posts.py
    test_update_post.py
  test_calculator.py
```

## Код дня

```python
# tests/api/conftest.py

@pytest.fixture(scope="module")
def api_client():
    return ApiClient("https://jsonplaceholder.typicode.com")
```

```python
# tests/conftest.py

@pytest.fixture(scope="function")
def sample_numbers():
    return [1, 2, 3, 4, 5]
```

## Команды дня

```powershell
git switch -c refactor/move-api-fixtures-to-api-conftest
.\.venv\Scripts\python.exe -m pytest tests/api
.\.venv\Scripts\python.exe -m pytest
```

## Результат

```text
23 passed
57 passed
```

## Новые слова

- `local conftest` - conftest.py внутри конкретной папки тестов.
- `test infrastructure` - вспомогательный код для тестов.
- `shared fixture` - общая фикстура.
- `local fixture` - фикстура для конкретной группы тестов.
- `scope of visibility` - область видимости.

## Правило дня

Фикстуры лучше хранить на том уровне папок, где они действительно нужны.

