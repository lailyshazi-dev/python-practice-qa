# День 26: первый POST-запрос в API-тестах

## Что я сделал

- Создал ветку `feature/add-post-api-test`.
- Добавил общий метод `post()` в `ApiClient`.
- Добавил метод `create_post()` для создания поста.
- Написал тест на статус ответа `201`.
- Написал тест на данные, которые API возвращает после POST-запроса.
- Столкнулся с ошибкой `ReadTimeout`.
- Увеличил timeout клиента с 5 до 10 секунд.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `GET` получает данные с сервера.
- `POST` отправляет данные на сервер.
- `payload` - это тело запроса, то есть данные, которые отправляются в API.
- Статус `201` обычно означает, что ресурс создан.
- Учебный API `jsonplaceholder` не создает данные по-настоящему, но возвращает ответ как будто объект создан.
- `ReadTimeout` означает, что сервер не успел ответить за заданное время.
- Timeout не ускоряет сеть, а ограничивает время ожидания.

## Код дня

```python
def post(self, path: str, json: dict):
    return requests.post(f"{self.base_url}{path}", json=json, timeout=self.timeout)

def create_post(self, payload: dict):
    return self.post("/posts", json=payload)
```

```python
def test_create_post_response_contains_sent_data(api_client):
    payload = {
        "title": "Test title",
        "body": "Test body",
        "userId": 1,
    }

    response = api_client.create_post(payload)
    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data
```

## Команды дня

```powershell
git switch -c feature/add-post-api-test
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
17 passed, 34 deselected
51 passed
```

## Новые слова

- `POST` - HTTP-запрос для отправки или создания данных.
- `payload` - данные, которые отправляются в запросе.
- `201 Created` - статус успешного создания ресурса.
- `ReadTimeout` - ошибка, когда сервер долго не отвечает.
- `fake API` - учебный API, который имитирует поведение настоящего сервера.

## Правило дня

POST-тест должен проверять не только статус ответа, но и то, что сервер вернул отправленные данные.

