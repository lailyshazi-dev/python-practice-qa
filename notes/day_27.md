# День 27: первый PUT-запрос в API-тестах

## Что я сделал

- Создал ветку `feature/add-put-api-test`.
- Добавил общий метод `put()` в `ApiClient`.
- Добавил метод `update_post()`.
- Написал тест на статус ответа после обновления поста.
- Написал тест на обновленные данные в ответе API.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `POST` обычно используется для создания нового ресурса.
- `PUT` обычно используется для полного обновления существующего ресурса.
- При `PUT` мы отправляем полный набор данных для ресурса.
- Статус `200` обычно означает успешное выполнение запроса.
- После обновления важно проверить не только статус, но и возвращенные данные.

## Код дня

```python
def put(self, path: str, json: dict):
    return requests.put(f"{self.base_url}{path}", json=json, timeout=self.timeout)

def update_post(self, post_id: int, payload: dict):
    return self.put(f"/posts/{post_id}", json=payload)
```

```python
def test_update_post_response_contains_updated_data(api_client):
    payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1,
    }

    response = api_client.update_post(1, payload)
    data = response.json()

    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
```

## Команды дня

```powershell
git switch -c feature/add-put-api-test
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
19 passed, 34 deselected
53 passed
```

## Новые слова

- `PUT` - HTTP-запрос для полного обновления ресурса.
- `update` - обновить.
- `resource` - сущность или объект API.
- `full replacement` - полная замена данных.
- `200 OK` - успешный ответ.

## Правило дня

После `PUT` нужно проверить и статус ответа, и то, что API вернул именно обновленные данные.

