# День 54: query parameters в API

## Что я сделал

- Создал ветку `feature/add-api-query-params`.
- Расширил метод `get`, добавив параметр `params`.
- Добавил метод `get_posts_by_user(user_id)`.
- Написал параметризованный тест для пользователей `1`, `5` и `10`.
- Проверил status code, непустой ответ и фильтрацию всех элементов.
- Запустил новый тест, API-набор и весь проект.
- Проверил изменения через `git diff --check`.

## Что понял

- Query parameters передаются после `?` в URL.
- Библиотека `requests` принимает их через аргумент `params`.
- Словарь `{"userId": 5}` превращается в `?userId=5`.
- `all(...)` проверяет условие для каждого элемента коллекции.
- Изменение общего метода `get` не сломало существующие вызовы, потому что `params` по умолчанию равен `None`.

## Где это нужно в реальной работе

- Фильтрация заказов по статусу: `?status=paid`.
- Получение товаров конкретной категории: `?category=phones`.
- Поиск пользователей: `?name=Ivan`.
- Сортировка: `?sort=price`.
- Пагинация: `?page=2&limit=20`.
- Получение данных конкретного владельца: `?userId=5`.

## Код дня

```python
def get(self, path: str, params: dict | None = None):
    return requests.get(
        f"{self.base_url}{path}",
        params=params,
        timeout=self.timeout,
    )

def get_posts_by_user(self, user_id: int):
    return self.get("/posts", params={"userId": user_id})
```

## Тест дня

```python
@pytest.mark.parametrize(
    "user_id",
    [
        pytest.param(1, id="first-user"),
        pytest.param(5, id="middle-user"),
        pytest.param(10, id="last-user"),
    ],
)
def test_get_posts_by_user_returns_only_requested_user(api_client, user_id):
    response = api_client.get_posts_by_user(user_id)
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0
    assert all(post["userId"] == user_id for post in data)
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/api/test_get_posts.py::test_get_posts_by_user_returns_only_requested_user -vv
.\.venv\Scripts\python.exe -m pytest tests/api
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
3 passed
26 passed
83 passed
git diff --check без ошибок
```

## Новые слова

- `query parameter` - параметр запроса в URL.
- `filtering` - фильтрация данных.
- `params` - аргумент requests для query parameters.
- `all` - проверка условия для всех элементов.
- `pagination` - получение данных частями, по страницам.

## Правило дня

Проверяя API-фильтр, недостаточно проверить status code: нужно убедиться, что каждый элемент ответа соответствует фильтру.
