# День 45: ids в параметризации pytest

## Что я сделал

- Создал ветку `refactor/add-parametrize-ids`.
- Добавил `ids` в параметризованный негативный тест.
- Запустил конкретный параметризованный тест в подробном режиме.
- Проверил, что в выводе pytest появились понятные имена сценариев.
- Запустил весь проект.

## Что понял

- `ids` задает понятные имена для наборов данных в `@pytest.mark.parametrize`.
- Без `ids` pytest может показывать менее удобные названия параметров.
- С `ids` в отчете сразу видно, какой именно сценарий выполнился или упал.
- Из-за `addopts = -q` в `pytest.ini` обычный `-v` может показывать недостаточно подробный вывод.
- Для просмотра имен параметризованных сценариев можно использовать `-vv`.

## Где это нужно в реальной работе

- В CI/CD падает параметризованный тест, и по `id` сразу видно проблемный сценарий.
- В HTML-отчете легче читать результаты, если кейсы называются `invalid-email`, `empty-password`, `short-password`.
- В API-тестах можно назвать payload-сценарии: `missing-title`, `empty-body`, `invalid-user-id`.
- В UI-тестах можно назвать проверки форм: `empty-login`, `wrong-password`, `blocked-user`.
- Хорошие `ids` экономят время на расследовании падений тестов.

## Код дня

```python
@pytest.mark.negative
@pytest.mark.parametrize(
    "numbers, expected_error",
    [
        ([], "Cannot calculate average of empty list"),
        (list(), "Cannot calculate average of empty list"),
    ],
    ids=["empty-list-literal", "empty-list-constructor"],
)
def test_list_average_with_empty_list_raises_error(numbers, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        list_average(numbers)
```

## Команды дня

```powershell
git switch -c refactor/add-parametrize-ids
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py::test_list_average_with_empty_list_raises_error -vv
.\.venv\Scripts\python.exe -m pytest
```

## Результат

```text
test_list_average_with_empty_list_raises_error[empty-list-literal] PASSED
test_list_average_with_empty_list_raises_error[empty-list-constructor] PASSED
59 passed
```

## Новые слова

- `ids` - понятные имена наборов данных в параметризации.
- `verbose` - подробный режим вывода.
- `-vv` - очень подробный вывод pytest.
- `readable report` - читаемый отчет.
- `test scenario name` - имя тестового сценария.

## Правило дня

Если параметризованный тест будет читаться в отчете, дай его наборам данных понятные `ids`.
