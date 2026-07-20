# День 56: requests.Session и общие headers

## Что я сделал

- Создал ветку `refactor/use-requests-session`.
- Создал `requests.Session` внутри `ApiClient`.
- Добавил общий header `Accept: application/json`.
- Перевел GET, POST, PUT, PATCH и DELETE на одну session.
- Добавил отдельный файл `tests/api/test_api_client.py`.
- Проверил тип session и значение общего header.
- Запустил API-тесты и весь проект.

## Что понял

- `requests.Session` хранит общие настройки между запросами.
- Session переиспользует соединения и может ускорить серию запросов.
- В session можно централизованно хранить headers, cookies и авторизацию.
- `Accept: application/json` сообщает серверу, что клиент ожидает JSON.
- При `json=payload` библиотека requests сама формирует JSON Content-Type.

## Где это нужно в реальной работе

- Все запросы к API используют один bearer token.
- После авторизации session сохраняет cookies.
- Общий header версии API задается один раз.
- Большой набор тестов переиспользует HTTP-соединения.
- Настройки клиента меняются в одном месте, а не в каждом тесте.

## Код дня

```python
class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
            }
        )
```

Пример использования session:

```python
def get(self, path: str, params: dict | None = None):
    return self.session.get(
        f"{self.base_url}{path}",
        params=params,
        timeout=self.timeout,
    )
```

## Тесты дня

```python
def test_api_client_uses_requests_session(api_client):
    assert isinstance(api_client.session, requests.Session), (
        f"Expected requests.Session, got {type(api_client.session).__name__}"
    )


def test_api_client_has_default_accept_header(api_client):
    assert api_client.session.headers["Accept"] == "application/json"
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/api/test_api_client.py -vv
.\.venv\Scripts\python.exe -m pytest tests/api
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
2 passed
32 passed
89 passed
git diff --check без ошибок
```

## Новые слова

- `session` - объект с общими настройками HTTP-запросов.
- `header` - служебная информация HTTP-запроса или ответа.
- `Accept` - формат ответа, который ожидает клиент.
- `connection pooling` - переиспользование сетевых соединений.
- `cookie persistence` - сохранение cookies между запросами.

## Правило дня

Общие headers, cookies и авторизацию лучше настраивать в одной Session, а не дублировать в каждом запросе.
