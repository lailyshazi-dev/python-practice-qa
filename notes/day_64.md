# День 64: Playwright base URL и UI fixture

## Что я сделал

- Создал ветку `refactor/playwright-ui-fixture`.
- Добавил `base_url` в `pytest.ini`.
- Создал `tests/ui/conftest.py`.
- Добавил fixture `todo_page`.
- Перенёс навигацию TodoMVC из тестов в fixture.
- Удалил повторяющийся `TODO_URL` из `test_todo_page.py`.
- Перевёл три теста на подготовленную страницу `todo_page`.
- Сохранил поведение тестов после рефакторинга.

## Конфигурация base URL

```ini
[pytest]
base_url = https://demo.playwright.dev/todomvc/
```

URL стенда больше не является частью каждого теста. Если тестовое окружение изменится, достаточно передать другой адрес:

```powershell
.\.venv\Scripts\python.exe -m pytest -m ui --base-url=https://new-test-environment.example.com/
```

Один и тот же тестовый код может работать на локальном, dev или stage-стенде.

## Fixture `todo_page`

```python
import pytest
from playwright.sync_api import Page


@pytest.fixture
def todo_page(page: Page, base_url: str):
    page.goto(base_url)

    return page
```

Fixture зависит от двух других fixtures:

```text
base_url ─┐
          ├─> todo_page ─> test
page ─────┘
```

pytest сам создаёт `page` и передаёт его в `todo_page`, затем возвращает подготовленную страницу тесту.

## Как теперь выглядит тест

```python
def test_user_can_add_todo(todo_page: Page):
    todo_input = todo_page.get_by_placeholder(
        "What needs to be done?"
    )

    todo_input.fill("Learn Playwright locators")
    todo_input.press("Enter")
```

В тесте осталась бизнес-логика пользователя. Техническая подготовка страницы находится в одном общем месте.

## Почему это рефакторинг

Поведение не изменилось:

```text
до:  каждый тест открывал TODO_URL
после: fixture открывает страницу один раз для каждого теста
```

Рефакторинг изменяет структуру и уменьшает дублирование, но сохраняет результат работы тестов.

Преимущества:

- один источник URL;
- одна точка для навигации;
- меньше повторяющегося кода;
- проще добавить авторизацию или очистку состояния;
- тесты читаются как пользовательские сценарии.

## Почему `conftest.py` находится в `tests/ui`

Fixture из `tests/ui/conftest.py` доступна тестам внутри этого каталога и его дочерних каталогов. Она не становится автоматически общей для API- и calculator-тестов.

Это полезная граница:

- `tests/conftest.py` — общие fixtures проекта;
- `tests/api/conftest.py` — fixtures API;
- `tests/ui/conftest.py` — fixtures браузера и UI.

Если fixture находится не в видимой для теста ветке каталогов, pytest сообщит:

```text
fixture 'todo_page' not found
```

## Scope по умолчанию

У `@pytest.fixture` без параметра `scope` используется `function` scope. Значит, для каждого теста создаётся отдельный экземпляр fixture.

Для UI это важно: каждый тест получает новую страницу и изолированное состояние browser context.

Другие scopes:

- `function` — один раз на тест;
- `class` — один раз на класс;
- `module` — один раз на файл;
- `package` — один раз на пакет;
- `session` — один раз на весь запуск.

Чем шире scope, тем меньше setup, но тем выше риск общего состояния между тестами.

## Где это нужно в реальной работе

Fixtures подготавливают:

- авторизованную страницу;
- API-клиент;
- тестового пользователя;
- подключение к базе;
- payload;
- временный файл;
- тестовую корзину;
- настройки окружения;
- browser context с нужным viewport.

Пример будущей UI-fixture:

```python
@pytest.fixture
def logged_in_page(page: Page, base_url: str):
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").fill("qa@example.com")
    page.get_by_label("Password").fill("test-password")
    page.get_by_role("button", name="Sign in").click()

    return page
```

Тест личного кабинета будет начинаться с готового состояния, а не повторять login в каждом сценарии.

## Почему нельзя бездумно использовать широкую fixture

Плохой пример — один session-scoped browser context для всех тестов. Тогда:

- cookies могут перейти между пользователями;
- local storage может загрязнить следующий тест;
- порядок тестов начнёт иметь значение;
- параллельный запуск станет опасным.

Широкий scope нужен только для действительно неизменяемых или безопасно разделяемых ресурсов.

## `return` и `yield`

Текущая fixture только подготавливает страницу и возвращает её:

```python
return page
```

Если нужен cleanup, используется `yield`:

```python
@pytest.fixture
def temporary_resource():
    resource = create_resource()

    yield resource

    delete_resource(resource)
```

Код после `yield` выполняется как teardown после теста, в том числе при падении теста.

В нашем API-проекте похожий подход уже используется для закрытия `ApiClient`:

```python
yield client
client.close()
```

## Проверка

```text
5 passed, 98 deselected — UI marker
103 passed — весь проект
git diff --check без ошибок
```

## Новые слова

- `fixture` — повторно используемая подготовка теста.
- `dependency injection` — передача зависимости тесту через аргумент.
- `scope` — время жизни fixture.
- `setup` — подготовка перед тестом.
- `teardown` — очистка после теста.
- `base URL` — общий начальный адрес приложения.
- `single source of truth` — одно место для настройки.

## Правило дня

Общие подготовительные действия выносим в fixture, а тест оставляем сосредоточенным на проверяемом поведении.
