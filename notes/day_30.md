# День 30: фикстуры для API test data

## Что я сделал

- Создал ветку `refactor/add-api-payload-fixtures`.
- Добавил фикстуры `new_post_payload`, `updated_post_payload`, `patched_post_payload`.
- Убрал повторяющиеся словари `payload` из API-тестов.
- Подключил тестовые данные через аргументы тестовых функций.
- Исправил ошибку, когда при рефакторинге потерялся аргумент `post_id`.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- Фикстуры можно использовать не только для клиентов и настроек, но и для тестовых данных.
- Если одни и те же данные повторяются в нескольких тестах, их лучше вынести в одно место.
- Это делает тесты короче и уменьшает копипасту.
- При рефакторинге важно следить не только за данными, но и за обязательными аргументами методов.
- Если метод ожидает `post_id` и `payload`, нужно передавать оба значения.

## Код дня

```python
@pytest.fixture
def new_post_payload():
    return {
        "title": "Test title",
        "body": "Test body",
        "userId": 1,
    }
```

```python
def test_create_post_response_contains_sent_data(api_client, new_post_payload):
    response = api_client.create_post(new_post_payload)
    data = response.json()

    assert data["title"] == new_post_payload["title"]
    assert data["body"] == new_post_payload["body"]
    assert data["userId"] == new_post_payload["userId"]
    assert "id" in data
```

## Команды дня

```powershell
git switch -c refactor/add-api-payload-fixtures
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
23 passed, 34 deselected
57 passed
```

## Новые слова

- `test data` - тестовые данные.
- `payload fixture` - фикстура с телом запроса.
- `duplication` - повторение кода.
- `copy-paste` - копирование одинакового кода.
- `required argument` - обязательный аргумент.

## Правило дня

Повторяющиеся тестовые данные лучше выносить в фикстуры, но при рефакторинге нельзя терять обязательные аргументы вызовов.

