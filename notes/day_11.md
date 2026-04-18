# День 11: pytest markers

## Что я сделал

- Создал ветку `feature/add-pytest-markers`.
- Добавил файл `pytest.ini` в корень проекта.
- Зарегистрировал маркеры `smoke`, `regression` и `negative`.
- Пометил часть тестов маркерами.
- Запустил все тесты.
- Запустил только `smoke` тесты.
- Запустил только `negative` тесты.
- Сделал merge в `master`.
- Отправил изменения на GitHub.

## Что понял

- Маркеры позволяют группировать тесты.
- Через `pytest -m marker_name` можно запускать только нужную группу.
- `deselected` означает тесты, которые pytest нашел, но не запустил из-за фильтра.
- `pytest.ini` хранит настройки pytest для проекта.
- Маркеры полезны для smoke, regression и negative наборов.

## Команды дня

```powershell
python -m pytest
python -m pytest -m smoke
python -m pytest -m negative
python -m pytest -m "not negative"
```

## Новые слова

- `marker` - метка теста.
- `smoke test` - быстрый критичный тест.
- `regression` - набор тестов для проверки старой функциональности.
- `deselected` - найден, но не выбран для запуска.
- `config` - конфигурация.

## Правило дня

Маркеры помогают запускать не все тесты подряд, а нужную группу под конкретную задачу.

