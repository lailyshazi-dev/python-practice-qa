# День 42: дополнительные негативные тесты

## Что я сделал

- Создал ветку `feature/add-more-error-tests`.
- Добавил негативный тест для деления отрицательного числа на ноль.
- Добавил негативный тест для пустого списка, сохраненного в переменную.
- Запустил только негативные calculator-тесты.
- Запустил все тесты проекта.

## Что понял

- `pytest.raises` проверяет, что функция падает с ожидаемой ошибкой.
- `match` проверяет текст ошибки.
- Негативные тесты проверяют неправильные или запрещенные данные.
- Один и тот же тип ошибки полезно проверять на разных входных данных.
- Тестовые данные можно сначала сохранить в переменную, а потом передать в функцию.

## Где это нужно в реальной работе

- API получает неверные данные и должен вернуть понятную ошибку.
- Форма регистрации получает пустой email или неправильный пароль.
- Пользователь пытается выполнить запрещенное действие.
- Backend должен не просто упасть, а вернуть ожидаемую причину ошибки.
- QA проверяет, что система одинаково корректно обрабатывает разные неправильные входные данные.

## Код дня

```python
@pytest.mark.negative
def test_divide_negative_number_by_zero_raises_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(-10, 0)
```

```python
@pytest.mark.negative
def test_list_average_with_another_empty_list_raises_error():
    empty_numbers = []

    with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
        list_average(empty_numbers)
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_calculator.py -m negative
.\.venv\Scripts\python.exe -m pytest
```

## Результат

```text
5 passed, 31 deselected
59 passed
```

## Новые слова

- `negative test` - тест на неправильные или запрещенные данные.
- `pytest.raises` - проверка ожидаемой ошибки.
- `match` - проверка текста ошибки.
- `test data` - тестовые данные.
- `edge case` - граничный или нестандартный случай.

## Правило дня

Негативный тест должен проверять не только факт ошибки, но и то, что ошибка ожидаемая и понятная.
