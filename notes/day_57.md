# День 57: teardown фикстуры и закрытие Session

## Что я сделал

- Создал ветку `refactor/close-api-session`.
- Добавил метод `ApiClient.close()`.
- Переделал fixture `api_client` с `return` на `yield`.
- Добавил teardown, который закрывает Session.
- Через `monkeypatch` проверил вызов `session.close()`.
- Перенес тест клиента в тематический файл `test_api_client.py`.
- Запустил API-тесты и весь проект.

## Что понял

- Fixture может не только создавать ресурс, но и очищать его.
- Код до `yield` выполняет setup.
- Значение из `yield` получают тесты.
- Код после `yield` выполняет teardown.
- `monkeypatch` временно заменяет объект или метод во время теста.
- Тесты нужно хранить в файле, соответствующем их ответственности.

## Где это нужно в реальной работе

- Закрытие браузера Playwright или Selenium.
- Закрытие HTTP Session.
- Отключение от базы данных.
- Удаление временных файлов и директорий.
- Очистка созданных пользователей, заказов и других тестовых данных.
- Освобождение ресурсов даже после падения теста.

## Код дня

```python
def close(self):
    self.session.close()
```

Fixture с teardown:

```python
@pytest.fixture(scope="module")
def api_client():
    client = ApiClient("https://jsonplaceholder.typicode.com")

    yield client

    client.close()
```

## Тест дня

```python
def test_api_client_close_calls_session_close(api_client, monkeypatch):
    close_calls = []

    def fake_close():
        close_calls.append("closed")

    monkeypatch.setattr(api_client.session, "close", fake_close)

    api_client.close()

    assert close_calls == ["closed"]
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
3 passed
33 passed
90 passed
git diff --check без ошибок
```

## Новые слова

- `setup` - подготовка перед тестами.
- `teardown` - очистка после тестов.
- `yield fixture` - fixture с подготовкой и очисткой.
- `monkeypatch` - временная замена объекта или поведения.
- `resource cleanup` - освобождение ресурсов.

## Правило дня

Если fixture создает внешний ресурс, она должна гарантированно освободить его в teardown.
