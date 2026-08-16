# День 73: параметризованный mock и обработка HTTP-сценариев

## Цель урока

Объединить параметризацию pytest и network mocking, чтобы одним тестом проверить успешный ответ, ошибку сервера и пустые данные.

## Что сделано

- Тест mock-ответа сделан параметризованным.
- Добавлены три сценария через `pytest.param`.
- Для каждого сценария передаются status code, payload и ожидаемое `response.ok`.
- Mock теперь сериализует именно текущий payload.
- Проверяется status, `ok` и JSON body.

## Набор сценариев

```python
@pytest.mark.parametrize(
    "status_code, payload, expected_ok",
    [
        pytest.param(
            200,
            {
                "status": "ok",
                "source": "mock",
            },
            True,
            id="success-response",
        ),
        pytest.param(
            500,
            {
                "error": "Internal Server Error",
            },
            False,
            id="server-error",
        ),
        pytest.param(
            200,
            {
                "items": [],
            },
            True,
            id="empty-list",
        ),
    ],
)
```

pytest создаёт три отдельных кейса:

```text
test_browser_can_use_mocked_api_response[success-response]
test_browser_can_use_mocked_api_response[server-error]
test_browser_can_use_mocked_api_response[empty-list]
```

## Динамический mock body

Первоначальная ошибка была логической: status code брался из параметра, но body оставался захардкоженным.

Плохой вариант:

```python
body='{"status": "ok", "source": "mock"}'
```

Такой mock не может вернуть `500` с ошибкой или пустой список.

Правильный вариант:

```python
body=json.dumps(payload)
```

Теперь каждый параметр реально управляет ответом. Это пример проверки не только синтаксиса, но и соответствия тестовых данных логике теста.

## `response.ok` и HTTP status

В браузерном Fetch HTTP-ответ `500` не обязательно приводит к исключению JavaScript. Fetch возвращает объект Response:

```javascript
{
    ok: false,
    status: 500,
}
```

Поэтому frontend должен сам проверить `response.ok` или `response.status` и показать состояние ошибки.

Для статусов `200–299` `response.ok` обычно `True`. Для `4xx` и `5xx` он `False`.

## HTTP-ошибка и network exception

HTTP-ошибка означает, что сервер ответил, но status показывает проблему: `400`, `401`, `404`, `500`.

Network exception означает, что ответ не был получен: DNS failure, connection refused, timeout или разрыв соединения.

Это разные ветки обработки и разные тестовые сценарии.

## Реальные сценарии

### Успешная загрузка

Backend возвращает `200` и список данных. UI показывает таблицу.

### Ошибка сервера

Backend возвращает `500`. UI показывает сообщение, кнопку повтора и не падает с JavaScript exception.

### Пустой результат

Backend возвращает `200` и пустой список. UI показывает empty state, а не ошибку сервера.

### Нет соединения

Ответ не приходит. UI показывает состояние offline или timeout. Такой сценарий требует отдельного network failure mock, например `route.abort()`.

## Почему параметризация полезна с mock

Без параметризации для трёх ответов пришлось бы писать три почти одинаковых теста. С параметризацией общими остаются:

- регистрация route;
- открытие страницы;
- browser fetch;
- проверка структуры результата.

Меняются только данные конкретного сценария.

## Результат проверки

```text
3 passed                 -- mock-кейсы
13 passed                -- UI-тесты
111 passed               -- весь проект
py_compile               -- без синтаксических ошибок
git diff --check         -- без ошибок
```

## Правило дня

Параметр должен управлять всем ожидаемым ответом; нельзя оставлять часть mock-данных захардкоженной.
