# День 14: первые API-тесты через requests

## Что я сделал

- Создал ветку `feature/add-api-tests`.
- Установил библиотеку `requests`.
- Обновил файл `requirements.txt`.
- Создал файл `tests/test_api_posts.py`.
- Написал первые API-тесты для `jsonplaceholder.typicode.com`.
- Проверил HTTP-статус ответа.
- Проверил поля в JSON-ответе.
- Проверил значение поля `id`.
- Запустил все тесты.

## Что понял

- API-тест проверяет ответ сервера без открытия браузера.
- `requests.get()` отправляет GET-запрос.
- `response.status_code` хранит HTTP-статус ответа.
- Код `200` означает, что запрос успешно обработан.
- `response.json()` превращает JSON-ответ в Python-словарь.
- Поля ответа можно проверять через обычные `assert`.

## Команды дня

```powershell
git switch -c feature/add-api-tests
.\.venv\Scripts\python.exe -m pip install requests
.\.venv\Scripts\python.exe -m pip freeze | Out-File -Encoding utf8 requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

## Код дня

```python
response = requests.get(f"{BASE_URL}/posts/1")
data = response.json()

assert response.status_code == 200
assert data["id"] == 1
```

## Результат

```text
37 passed
```

## Новые слова

- `API` - способ общения программ друг с другом.
- `HTTP` - протокол, по которому браузер и программы общаются с сервером.
- `GET` - запрос на получение данных.
- `status code` - код ответа сервера.
- `JSON` - формат данных, похожий на Python-словарь.
- `response` - ответ сервера.
- `endpoint` - конкретный адрес API.

## Правило дня

API-тест должен проверять не только что сервер ответил, но и что в ответе есть нужные данные.

