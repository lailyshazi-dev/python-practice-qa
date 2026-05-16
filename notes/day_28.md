# День 28: первый PATCH-запрос в API-тестах

## Что я сделал

- Создал ветку `feature/add-patch-api-test`.
- Добавил общий метод `patch()` в `ApiClient`.
- Добавил метод `patch_post()`.
- Написал тест на статус ответа после частичного обновления поста.
- Написал тест на обновленное поле в ответе API.
- Разобрал разницу между `PUT` и `PATCH`.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `PUT` обычно обновляет ресурс целиком.
- `PATCH` обычно обновляет только часть ресурса.
- При `PATCH` можно отправить только измененные поля.
- `PATCH` относится к данным на сервере, а не к обновлению части HTML-страницы напрямую.
- Фронтенд сам решает, какую часть интерфейса обновить после ответа сервера.

## Код дня

```python
def patch(self, path: str, json: dict):
    return requests.patch(f"{self.base_url}{path}", json=json, timeout=self.timeout)

def patch_post(self, post_id: int, payload: dict):
    return self.patch(f"/posts/{post_id}", json=payload)
```

```python
def test_patch_post_response_contains_updated_field(api_client):
    payload = {
        "title": "Patched title",
    }

    response = api_client.patch_post(1, payload)
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == payload["title"]
```

## Команды дня

```powershell
git switch -c feature/add-patch-api-test
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
21 passed, 34 deselected
55 passed
```

## Новые слова

- `PATCH` - HTTP-запрос для частичного обновления ресурса.
- `partial update` - частичное обновление.
- `field` - отдельное поле объекта.
- `frontend` - клиентская часть приложения, которую видит пользователь.
- `rerender` - перерисовать часть интерфейса.

## Правило дня

Если нужно изменить только часть данных ресурса, чаще подходит `PATCH`, а не `PUT`.

