# День 17: API fixtures

## Что я сделал

- Создал ветку `refactor/add-api-client-fixture`.
- Добавил класс `ApiClient` в `tests/conftest.py`.
- Добавил фикстуру `api_client`.
- Убрал прямые вызовы `requests.get()` из API-тестов.
- Заменил прямые запросы на `api_client.get_post(...)`.
- Исправил ошибку `NameError: name 'api_client' is not defined`.
- Запустил все тесты проекта.

## Что понял

- Фикстура может готовить объект для тестов.
- API-клиент помогает убрать повторение из тестов.
- `conftest.py` подходит для общих фикстур, которые нужны разным тестовым файлам.
- Чтобы использовать фикстуру в тесте, ее имя нужно указать в аргументах тестовой функции.
- Если внутри теста написано `api_client`, но в аргументах функции нет `api_client`, будет ошибка `NameError`.

## Код дня

```python
class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_post(self, post_id: int):
        return requests.get(f"{self.base_url}/posts/{post_id}")
```

```python
@pytest.fixture(scope="module")
def api_client():
    return ApiClient("https://jsonplaceholder.typicode.com")
```

```python
def test_get_post_by_id_status_code(api_client):
    response = api_client.get_post(1)

    assert response.status_code == 200
```

## Команды дня

```powershell
git switch -c refactor/add-api-client-fixture
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
44 passed
```

## Новые слова

- `API client` - объект, через который тесты отправляют API-запросы.
- `base_url` - базовый адрес API.
- `method` - функция внутри класса.
- `NameError` - ошибка, когда Python не знает имя переменной или объекта.
- `refactor` - изменение структуры кода без изменения поведения.

## Правило дня

Фикстура работает в тесте только тогда, когда ее имя указано в аргументах тестовой функции.

