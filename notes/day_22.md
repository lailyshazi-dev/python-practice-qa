# День 22: timeout для API-запросов

## Что я сделал

- Создал ветку `refactor/add-api-timeout`.
- Добавил параметр `timeout` в класс `ApiClient`.
- Сохранил `timeout` внутри объекта клиента.
- Передал `timeout` в методы `requests.get(...)`.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `timeout` ограничивает время ожидания ответа от сервера.
- Без `timeout` HTTP-запрос может ждать слишком долго.
- Таймаут защищает автотесты от зависания.
- Значение `timeout=5` означает ожидать ответ не дольше 5 секунд.
- Если сервер не отвечает вовремя, `requests` выбросит ошибку.
- В реальных API-тестах таймауты почти всегда нужны.

## Код дня

```python
class ApiClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url
        self.timeout = timeout

    def get_post(self, post_id: int):
        return requests.get(f"{self.base_url}/posts/{post_id}", timeout=self.timeout)

    def get_posts(self):
        return requests.get(f"{self.base_url}/posts", timeout=self.timeout)
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
14 passed, 34 deselected
48 passed
```

## Новые слова

- `timeout` - ограничение времени ожидания.
- `hang` - зависнуть.
- `request timeout` - ошибка из-за слишком долгого ожидания ответа.
- `network issue` - проблема с сетью.
- `default value` - значение по умолчанию.

## Правило дня

API-запрос в автотестах должен иметь timeout, чтобы тестовый запуск не зависал из-за проблем с сетью или сервером.

