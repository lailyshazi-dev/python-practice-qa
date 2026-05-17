# День 29: первый DELETE-запрос в API-тестах

## Что я сделал

- Создал ветку `feature/add-delete-api-test`.
- Добавил общий метод `delete()` в `ApiClient`.
- Добавил метод `delete_post()`.
- Написал тест на статус ответа после удаления поста.
- Написал тест на пустое тело ответа после удаления.
- Разобрал, где `DELETE` используется в реальных приложениях.
- Запустил только API-тесты.
- Запустил все тесты проекта.

## Что понял

- `DELETE` нужен для удаления существующего ресурса.
- Это не изменение одного поля и не полное обновление объекта, а удаление самого объекта.
- После удаления API может вернуть `200`, `202` или `204` в зависимости от реализации.
- После успешного удаления ресурс обычно больше не должен быть доступен.
- Примеры: удалить комментарий, адрес доставки, товар из корзины, черновик или банковскую карту.

## Код дня

```python
def delete(self, path: str):
    return requests.delete(f"{self.base_url}{path}", timeout=self.timeout)

def delete_post(self, post_id: int):
    return self.delete(f"/posts/{post_id}")
```

```python
def test_delete_post_returns_empty_body(api_client):
    response = api_client.delete_post(1)
    data = response.json()

    assert data == {}
```

## Команды дня

```powershell
git switch -c feature/add-delete-api-test
.\.venv\Scripts\python.exe -m pytest -m api -q
.\.venv\Scripts\python.exe -m pytest -q
```

## Результат

```text
23 passed, 34 deselected
57 passed
```

## Новые слова

- `DELETE` - HTTP-запрос для удаления ресурса.
- `resource` - объект, с которым работает API.
- `204 No Content` - успешный ответ без тела.
- `remove` - удалить.
- `cart item` - товар в корзине.

## Правило дня

`DELETE` используют, когда нужно убрать ресурс целиком, а не просто изменить его отдельные поля.

