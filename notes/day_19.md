# День 19: проверка структуры объектов в API-списке

## Что я сделал

- Создал ветку `feature/validate-posts-list-structure`.
- Добавил тест на наличие обязательных полей у каждого поста.
- Добавил тест на типы значений у каждого поста.
- Проверил поля `userId`, `id`, `title`, `body`.
- Запустил только API-тесты.
- Запустил все тесты проекта.
- Разобрал, почему API-тесты медленнее локальных unit-тестов.

## Что понял

- Проверить, что API вернул список, недостаточно.
- Важно проверять структуру каждого объекта в списке.
- `for post in data` позволяет пройти по каждому объекту ответа.
- `isinstance(value, type)` проверяет тип значения.
- API-тесты часто медленнее unit-тестов, потому что делают HTTP-запросы по сети.
- Общее время запуска может зависеть не от количества тестов, а от того, какие тесты самые медленные.

## Код дня

```python
def test_get_posts_items_have_expected_fields(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert "userId" in post
        assert "id" in post
        assert "title" in post
        assert "body" in post
```

```python
def test_get_posts_items_have_expected_types(api_client):
    response = api_client.get_posts()
    data = response.json()

    for post in data:
        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_api_posts.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py -q
```

## Результат

```text
14 passed
48 passed
34 passed in 0.12s
```

## Новые слова

- `structure` - структура данных.
- `field` - поле объекта.
- `type` - тип данных.
- `isinstance` - проверка типа.
- `unit test` - быстрый локальный тест маленькой части кода.
- `network delay` - задержка из-за сети.

## Правило дня

API-тест списка должен проверять не только сам список, но и структуру объектов внутри него.

