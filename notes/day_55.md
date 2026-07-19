# День 55: API-пагинация

## Что я сделал

- Создал ветку `feature/add-api-pagination`.
- Добавил метод `get_posts_page(page, limit)`.
- Передал два query parameters: `_page` и `_limit`.
- Добавил три параметризованных сценария пагинации.
- Проверил размер страницы и id первого элемента.
- Добавил проверку страницы за пределами доступных данных.
- Запустил целевые тесты, API-набор и весь проект.

## Что понял

- Пагинация делит большой список на страницы.
- `_page` выбирает номер страницы.
- `_limit` ограничивает количество элементов.
- Несколько query parameters передаются одним словарем `params`.
- Для проверки страницы недостаточно проверить только status code.
- Пустая страница может быть корректным результатом со статусом `200`.

## Где это нужно в реальной работе

- Каталог интернет-магазина разбивается на страницы товаров.
- Лента сообщений загружает данные частями.
- История платежей показывает ограниченное количество операций.
- Административная панель загружает пользователей постранично.
- API защищается от передачи слишком большого ответа одним запросом.

## Код дня

```python
def get_posts_page(self, page: int, limit: int):
    return self.get(
        "/posts",
        params={"_page": page, "_limit": limit},
    )
```

## Позитивный тест

```python
@pytest.mark.parametrize(
    "page, limit, expected_first_id",
    [
        pytest.param(1, 5, 1, id="first-page"),
        pytest.param(2, 5, 6, id="second-page"),
        pytest.param(4, 10, 31, id="fourth-page"),
    ],
)
def test_get_posts_page_returns_expected_items(
    api_client,
    page,
    limit,
    expected_first_id,
):
    response = api_client.get_posts_page(page, limit)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == limit
    assert data[0]["id"] == expected_first_id
```

## Проверка пустой страницы

```python
@pytest.mark.negative
def test_get_posts_page_out_of_range_returns_empty_list(api_client):
    response = api_client.get_posts_page(page=100, limit=10)
    data = response.json()

    assert response.status_code == 200
    assert data == []
```

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pytest tests/api/test_get_posts.py -k "posts_page" -vv
.\.venv\Scripts\python.exe -m pytest tests/api
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

## Результат

```text
4 passed
30 passed
87 passed
git diff --check без ошибок
```

## Новые слова

- `pagination` - постраничная выдача данных.
- `page` - номер страницы.
- `limit` - максимальное количество элементов.
- `out of range` - значение за доступными границами.
- `empty result` - корректный пустой результат.

## Правило дня

Тест пагинации должен проверять status code, размер страницы, порядок данных и поведение за последней страницей.
