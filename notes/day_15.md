# День 15: параметризация API-тестов

## Что я сделал

- Создал ветку `feature/parametrize-api-tests`.
- Добавил импорт `pytest` в файл `tests/test_api_posts.py`.
- Добавил параметризованный API-тест.
- Проверил несколько постов одним тестом.
- Запустил все тесты в коротком режиме.
- Запустил API-тесты в подробном режиме.

## Что понял

- Параметризация позволяет запускать один тест с разными данными.
- `@pytest.mark.parametrize` передает значения в аргумент тестовой функции.
- Один тест может превратиться в несколько проверок.
- В подробном режиме `-v` pytest показывает параметры в имени теста.
- Запись вида `test_name[1]` означает, что тест был запущен с параметром `1`.

## Код дня

```python
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post_by_id_parametrized(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == post_id
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest tests/test_api_posts.py -v
```

## Результат

```text
42 passed
8 passed for tests/test_api_posts.py
```

## Новые слова

- `parametrize` - параметризовать, запускать тест с разными данными.
- `parameter` - параметр, значение для теста.
- `test data` - тестовые данные.
- `endpoint` - конкретный адрес API.
- `verbose output` - подробный вывод.

## Правило дня

Если проверка одинаковая, а данные разные, лучше использовать параметризацию вместо копирования тестов.

