# День 16: негативные API-тесты

## Что я сделал

- Создал ветку `feature/add-negative-api-tests`.
- Добавил негативный API-тест на несуществующий пост.
- Проверил, что API возвращает статус `404`.
- Проверил, что тело ответа для несуществующего поста пустое.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- Негативный тест проверяет неправильный или невозможный сценарий.
- Если ресурс не найден, сервер обычно возвращает HTTP-статус `404`.
- Негативный тест проходит, если система правильно обработала ошибочную ситуацию.
- API-тест может проверять не только статус ответа, но и тело ответа.
- Пустой JSON-объект в Python выглядит как `{}`.

## Код дня

```python
def test_get_missing_post_returns_404():
    response = requests.get(f"{BASE_URL}/posts/999999")

    assert response.status_code == 404


def test_get_missing_post_returns_empty_body():
    response = requests.get(f"{BASE_URL}/posts/999999")
    data = response.json()

    assert data == {}
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_api_posts.py -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
10 passed
44 passed
```

## Новые слова

- `negative test` - тест неправильного или невозможного сценария.
- `404 Not Found` - ресурс не найден.
- `empty body` - пустое тело ответа.
- `response body` - тело ответа сервера.
- `missing resource` - отсутствующий ресурс.

## Правило дня

Хороший API-набор проверяет не только успешные ответы, но и правильную обработку ошибок.

