# День 58: Bearer token в API-клиенте

## Что я сделал

- Создал ветку `feature/add-api-auth-header`.
- Добавил необязательный параметр `token` в `ApiClient`.
- Настроил общий Authorization header в Session.
- Добавил fixture с безопасным фиктивным token.
- Проверил клиента с token и без token.
- Разобрал каскадное падение из-за неправильного порядка инициализации.
- Запустил тесты клиента, API-набор и весь проект.

## Что понял

- Bearer token передается через HTTP header `Authorization`.
- Общий token удобно задавать один раз в Session.
- Неавторизованный клиент не должен получать Authorization header.
- Объект нужно создать до первого обращения к нему.
- Одна ошибка в `__init__` может вызвать много связанных падений.
- Исправлять нужно корневую причину, а не каждый упавший тест отдельно.

## Где это нужно в реальной работе

- Доступ к профилю пользователя.
- Создание и изменение заказов.
- Административные API endpoints.
- Проверка ролей и разрешений.
- Запуск тестов с token из CI/CD secrets.
- Проверка ответов `401 Unauthorized` и `403 Forbidden`.

Настоящие токены нельзя хранить в исходном коде или публиковать на GitHub.

## Код дня

```python
def __init__(
    self,
    base_url: str,
    timeout: int = 10,
    token: str | None = None,
):
    self.base_url = base_url
    self.timeout = timeout
    self.session = requests.Session()
    self.session.headers.update(
        {
            "Accept": "application/json",
        }
    )

    if token:
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
            }
        )
```

## Ошибка дня

Сначала настройка token выполнялась раньше создания Session:

```python
if token:
    self.session.headers.update(...)
```

При этом `self.session` еще не существовала. Это вызвало:

```text
AttributeError: 'ApiClient' object has no attribute 'session'
```

Из одной причины получилось `4 failed` и `2 errors`.

## Тесты дня

```python
def test_api_client_adds_bearer_token_header(authorized_api_client):
    assert (
        authorized_api_client.session.headers["Authorization"]
        == "Bearer test-token"
    )


def test_api_client_without_token_has_no_authorization_header(api_client):
    assert "Authorization" not in api_client.session.headers
```

## Результат

```text
5 passed
35 passed
92 passed
git diff --check без ошибок
```

## Новые слова

- `Bearer token` - token доступа в Authorization header.
- `Authorization` - HTTP header с данными авторизации.
- `root cause` - корневая причина проблемы.
- `cascade failure` - несколько падений из одной причины.
- `secret` - конфиденциальное значение.

## Правило дня

Сначала создавай и настраивай базовые поля объекта, затем используй их для дополнительных настроек.
