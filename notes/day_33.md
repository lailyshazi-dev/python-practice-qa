# День 33: отдельная папка tests/api для API-тестов

## Что я сделал

- Создал ветку `refactor/move-api-tests-to-folder`.
- Создал папку `tests/api`.
- Перенес API-тесты из общей папки `tests/` в `tests/api/`.
- Переименовал файлы так, чтобы внутри папки `api` не повторять слово `api` в каждом имени.
- Проверил запуск API-тестов по папке.
- Проверил запуск API-тестов по маркеру `api`.
- Запустил все тесты проекта.
- Столкнулся с `ReadTimeout` от внешнего учебного API и повторно подтвердил, что это не ошибка структуры.

## Что понял

- Тесты можно структурировать не только по файлам, но и по папкам.
- Папка `tests/api/` явно показывает, где лежат API-тесты.
- Запуск по папке и запуск по маркеру решают разные задачи.
- `pytest tests/api` запускает тесты из конкретной папки.
- `pytest -m api` запускает все тесты с маркером `api`, где бы они ни лежали.
- Перенос файлов без изменения поведения тестов - это рефакторинг.

## Где это нужно в реальной работе

- В большом проекте могут быть папки `tests/api`, `tests/ui`, `tests/mobile`, `tests/integration`.
- API-команда может запускать только `tests/api`, не трогая UI-тесты.
- В CI можно сделать отдельные jobs: один для API-тестов, другой для UI-тестов.
- Новому человеку в проекте проще понять структуру, если тесты разложены по слоям приложения.
- При code review проще увидеть, что изменение касается только API-тестов, а не всего тестового проекта.

## Новая структура

```text
tests/
  api/
    test_create_post.py
    test_delete_post.py
    test_get_posts.py
    test_update_post.py
  conftest.py
  test_calculator.py
```

## Команды дня

```powershell
git switch -c refactor/move-api-tests-to-folder
mkdir tests\api
Move-Item tests\test_api_get_posts.py tests\api\test_get_posts.py
Move-Item tests\test_api_create_post.py tests\api\test_create_post.py
Move-Item tests\test_api_update_post.py tests\api\test_update_post.py
Move-Item tests\test_api_delete_post.py tests\api\test_delete_post.py
.\.venv\Scripts\python.exe -m pytest tests\api -q
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
23 passed
23 passed, 34 deselected
57 passed
```

## Новые слова

- `folder structure` - структура папок.
- `test layer` - слой тестов.
- `CI job` - отдельная задача в CI.
- `move` - переместить.
- `path-based run` - запуск тестов по пути к папке или файлу.

## Правило дня

Когда появляются разные типы тестов, их удобно разделять не только маркерами, но и физически по папкам.

