# День 71: проверка network-ответа в UI-тесте

## Цель урока

Проверить, что действие браузера приводит не только к ожидаемому UI-состоянию, но и к успешному HTTP-ответу.

## Что сделано

- Создан `tests/ui/test_network.py`.
- Добавлен UI-маркер.
- Использован `page.expect_response()`.
- Проверены URL и HTTP-метод ожидаемого ответа.
- Проверены `response.ok` и status code `200`.
- Проверен итоговый URL TodoMVC с hash-маршрутом `#/`.

## Ожидание ответа

```python
with page.expect_response(
    lambda response: (
        response.url == base_url
        and response.request.method == "GET"
    )
) as response_info:
    page.goto(base_url)

response = response_info.value
```

Контекстный менеджер устанавливается до `page.goto()`, потому что именно переход вызывает network-событие.

## Проверка браузерного Response

```python
assert response.ok
assert response.status == 200
```

`page.expect_response()` возвращает браузерный `Response`. Для него используются свойства `ok`, `status`, `url` и `request`.

Важно не путать его с `APIResponse`. `expect(response).to_be_ok()` относится к APIResponse, который можно получить через `page.request` или API-клиент. Для сетевого ответа страницы применяются обычные проверки свойств.

## Hash-маршрут SPA

После загрузки TodoMVC фактический URL стал:

```text
https://demo.playwright.dev/todomvc/#/
```

Приложение использует client-side routing и добавляет `#/`. Поэтому проверяется:

```python
expect(page).to_have_url(
    f"{base_url}#/"
)
```

Это не ошибка `base_url`: начальный адрес и итоговый маршрут могут отличаться.

## UI-проверка и network-проверка

UI-проверка отвечает на вопрос: пользователь видит нужное состояние?

```python
expect(page.get_by_role("heading")).to_be_visible()
```

Network-проверка отвечает на вопрос: браузер получил ожидаемый ответ?

```python
assert response.ok
assert response.status == 200
```

Обе проверки дополняют друг друга. Страница может выглядеть правильно из cache, а API при этом вернуть ошибку. Или API ответит `200`, но JavaScript не отобразит данные.

## Реальные примеры

### Авторизация

```python
with page.expect_response("**/api/login") as response_info:
    page.get_by_role("button", name="Sign in").click()

response = response_info.value
assert response.status == 200
```

После этого отдельно проверяют появление профиля.

### Создание заказа

После нажатия `Submit` ожидают `POST /api/orders`, status `201` и страницу подтверждения.

### Обновление списка

После нажатия `Refresh` можно проверить `GET /api/items`, status `200`, а затем количество элементов на странице.

## Типичные ошибки

- Устанавливать `expect_response` после действия.
- Ждать слишком общий URL и поймать не тот запрос.
- Проверять только status code без UI-результата.
- Путать browser `Response` и `APIResponse`.
- Ожидать POST там, где приложение изменяет состояние только локально.
- Сравнивать URL SPA без учёта `#/` или другого client-side маршрута.

## Результат проверки

```text
1 passed                 -- network-тест
10 passed                -- UI-тесты
108 passed               -- весь проект
git diff --check         -- без ошибок
```

## Правило дня

Для важного пользовательского действия проверяй и сетевой контракт, и видимый результат интерфейса.

## Источники

- https://playwright.dev/python/docs/network
- https://playwright.dev/python/docs/api/class-page#page-expect-response
