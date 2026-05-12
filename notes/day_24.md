# День 24: проверка времени ответа API

## Что я сделал

- Создал ветку `feature/check-api-response-time`.
- Добавил тест на время ответа API.
- Использовал `response.elapsed`.
- Проверил время ответа через `total_seconds()`.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- API-тест может проверять не только статус и тело ответа.
- `response.elapsed` хранит время выполнения запроса.
- `response.elapsed.total_seconds()` возвращает время в секундах.
- Проверка времени ответа помогает заметить слишком медленный API.
- Такие тесты могут быть нестабильными, потому что зависят от сети.
- Нестабильный тест называют `flaky test`.

## Код дня

```python
def test_get_posts_response_time_is_less_than_one_second(api_client):
    response = api_client.get_posts()

    assert response.elapsed.total_seconds() < 1
```

## Команды дня

```powershell
git switch -c feature/check-api-response-time
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
15 passed, 34 deselected
49 passed
```

## Новые слова

- `response time` - время ответа.
- `elapsed` - прошедшее время.
- `total_seconds` - общее время в секундах.
- `performance` - производительность.
- `flaky test` - нестабильный тест, который иногда проходит, а иногда падает.

## Правило дня

Проверка времени ответа полезна, но лимит должен быть разумным, чтобы тест не падал случайно из-за сети.

