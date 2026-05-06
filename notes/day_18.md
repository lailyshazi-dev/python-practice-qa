# День 18: методы API-клиента и тест списка постов

## Что я сделал

- Создал ветку `feature/add-api-client-list-method`.
- Добавил метод `get_posts()` в класс `ApiClient`.
- Написал тест на статус ответа списка постов.
- Написал тест на то, что API возвращает список.
- Проверил, что список постов не пустой.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- API-клиент может содержать несколько методов для разных endpoint.
- Метод `get_post(post_id)` получает один пост.
- Метод `get_posts()` получает список постов.
- `isinstance(data, list)` проверяет, что данные являются списком.
- `len(data) > 0` проверяет, что список не пустой.
- Тесты коллекций важны, потому что API часто возвращает не один объект, а список объектов.

## Код дня

```python
def get_posts(self):
    return requests.get(f"{self.base_url}/posts")
```

```python
def test_get_posts_returns_list(api_client):
    response = api_client.get_posts()
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
```

## Команды дня

```powershell
git switch -c feature/add-api-client-list-method
.\.venv\Scripts\python.exe -m pytest tests/test_api_posts.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
12 passed
46 passed
```

## Новые слова

- `collection` - коллекция, набор объектов.
- `list` - список.
- `length` - длина.
- `isinstance` - проверка типа объекта.
- `endpoint method` - метод клиента для конкретного API-адреса.

## Правило дня

Когда API возвращает список, тест должен проверить не только статус ответа, но и то, что данные действительно являются непустым списком.

