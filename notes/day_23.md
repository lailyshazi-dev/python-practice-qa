# День 23: общий метод запроса в API-клиенте

## Что я сделал

- Создал ветку `refactor/add-api-get-helper`.
- Добавил общий метод `get(path)` в класс `ApiClient`.
- Переписал `get_post()` через общий метод `get()`.
- Переписал `get_posts()` через общий метод `get()`.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- Общую логику лучше хранить в одном месте.
- Метод `get()` отвечает за отправку GET-запроса.
- Методы `get_post()` и `get_posts()` теперь только передают нужный путь.
- Если позже нужно добавить логирование, обработку ошибок или retry, это можно будет сделать в одном методе `get()`.
- Такой рефакторинг не меняет поведение тестов, а улучшает структуру кода.

## Код дня

```python
def get(self, path: str):
    return requests.get(f"{self.base_url}{path}", timeout=self.timeout)
```

```python
def get_post(self, post_id: int):
    return self.get(f"/posts/{post_id}")

def get_posts(self):
    return self.get("/posts")
```

## Команды дня

```powershell
git switch -c refactor/add-api-get-helper
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
14 passed, 34 deselected
48 passed
```

## Новые слова

- `helper method` - вспомогательный метод.
- `path` - путь API после базового адреса.
- `delegate` - передать выполнение другой функции или методу.
- `refactor` - улучшение структуры кода без изменения поведения.
- `single place` - одно место, где хранится общая логика.

## Правило дня

Если одна и та же логика повторяется в нескольких методах, ее лучше вынести в один общий метод.

