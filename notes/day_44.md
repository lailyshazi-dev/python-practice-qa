# День 44: параметризация с ожидаемым текстом ошибки

## Что я сделал

- Создал ветку `refactor/parametrize-error-message-tests`.
- Нашел два похожих негативных теста для `list_average`.
- Объединил их в один параметризованный тест.
- Передал в параметризацию не только входные данные, но и ожидаемый текст ошибки.
- Запустил негативные calculator-тесты.
- Запустил все тесты проекта.

## Что понял

- В `@pytest.mark.parametrize` можно передавать несколько параметров.
- Тест может получать входные данные и ожидаемый результат одновременно.
- Для негативных тестов ожидаемым результатом часто является текст ошибки.
- `pytest.raises(..., match=expected_error)` проверяет, что ошибка не только произошла, но и содержит нужный текст.
- Такой подход делает тесты короче и удобнее для расширения.

## Где это нужно в реальной работе

- Форма регистрации проверяет разные ошибки: пустой email, неправильный email, короткий пароль.
- API возвращает разные сообщения для разных неправильных payload.
- Backend должен объяснять причину отказа, а не просто возвращать общую ошибку.
- QA Automation Engineer может добавить новый негативный сценарий одной строкой в список параметров.
- В CI/CD отчет сразу показывает, на каком наборе данных упала проверка.

## Код дня

```python
@pytest.mark.negative
@pytest.mark.parametrize(
    "numbers, expected_error",
    [
        ([], "Cannot calculate average of empty list"),
        (list(), "Cannot calculate average of empty list"),
    ],
)
def test_list_average_with_empty_list_raises_error(numbers, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        list_average(numbers)
```

## Как это читать

- `numbers` - данные, которые передаем в функцию.
- `expected_error` - текст ошибки, который ожидаем.
- `pytest.raises` - проверяет тип ошибки.
- `match=expected_error` - проверяет текст ошибки.

## Команды дня

```powershell
git switch -c refactor/parametrize-error-message-tests
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py -m negative
.\.venv\Scripts\python.exe -m pytest
```

## Результат

```text
5 passed, 31 deselected
59 passed
```

## Новые слова

- `expected_error` - ожидаемый текст ошибки.
- `validation error` - ошибка валидации данных.
- `payload` - данные, которые отправляются в API.
- `scenario` - тестовый сценарий.
- `extend` - расширять, добавлять новые случаи.

## Правило дня

Если разные негативные сценарии отличаются входными данными и текстом ошибки, удобно хранить их в параметрах теста.
