# День 60: базовый URL API из переменной окружения

## Что я сделал

- Создал ветку `feature/load-api-base-url-from-env`.
- Добавил константу `DEFAULT_API_BASE_URL`.
- Добавил функцию `get_api_base_url()`.
- Научил API fixture получать адрес сервера из конфигурации.
- Написал тест для заданной переменной `API_BASE_URL`.
- Написал тест для значения по умолчанию.
- Нашёл и удалил случайный дубликат тестового файла.
- Проверил config, API-набор и весь проект.

## Код урока

```python
import os


DEFAULT_API_BASE_URL = "https://jsonplaceholder.typicode.com"


def get_api_base_url() -> str:
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
```

Использование в fixture:

```python
@pytest.fixture(scope="module")
def api_client():
    client = ApiClient(get_api_base_url())

    yield client

    client.close()
```

Теперь тесты не привязаны напрямую к одному адресу внутри fixture.

## Что я понял

Второй аргумент `os.getenv()` является значением по умолчанию:

```python
os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
```

- Если `API_BASE_URL` существует, Python вернёт её значение.
- Если переменная отсутствует, Python вернёт `DEFAULT_API_BASE_URL`.

Token является секретом, поэтому для него безопаснее вернуть `None`, если настройка отсутствует. Тестовый URL не является секретом, поэтому для учебного проекта у него может быть публичное значение по умолчанию.

## Где это нужно в реальной работе

Один набор автотестов запускают на разных окружениях:

```text
dev   -> https://dev-api.example.com
stage -> https://stage-api.example.com
prod  -> https://api.example.com
```

Код не изменяется. Меняется только конфигурация запуска:

```powershell
$env:API_BASE_URL = "https://stage-api.example.com"
.\.venv\Scripts\python.exe -m pytest
```

Реальные применения:

- разработчик проверяет новую функцию на `dev`;
- QA запускает регрессию на `stage`;
- CI/CD выбирает адрес стенда из настроек pipeline;
- smoke-тесты проверяют production после релиза;
- локальный mock server подставляется вместо внешнего API.

На production опасные изменяющие тесты запускают только при явном разрешении. Одной возможности выбрать URL недостаточно: нужны ограничения и отдельная конфигурация безопасного набора тестов.

## Тесты конфигурации

Проверка явно заданного адреса:

```python
def test_get_api_base_url_returns_environment_value(monkeypatch):
    monkeypatch.setenv(
        "API_BASE_URL",
        "https://stage-api.example.com",
    )

    assert get_api_base_url() == "https://stage-api.example.com"
```

Проверка fallback:

```python
def test_get_api_base_url_returns_default_when_missing(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)

    assert get_api_base_url() == DEFAULT_API_BASE_URL
```

Оба теста изолированы от реального окружения компьютера. `monkeypatch` восстанавливает переменные после завершения каждого теста.

## Ошибка дня: дубликат файла

Правильный файл уже находился здесь:

```text
tests/test_config.py
```

Но случайно появился полный дубликат:

```text
tests/api/test_config.py
```

Дубликат мог привести к повторному запуску одинаковых тестов и ложному увеличению их количества. Он был удалён.

Правило структуры:

- `src/config.py` содержит рабочий код конфигурации;
- `tests/test_config.py` проверяет конфигурацию;
- `tests/api/` содержит тесты HTTP API;
- `tests/api/conftest.py` содержит fixtures для API-тестов.

## Результат

```text
4 passed — тесты config
35 passed, 61 deselected — API marker
96 passed — весь проект
git diff --check без ошибок
```

## Новые слова

- `base URL` — общая начальная часть адреса API.
- `environment` — окружение запуска: dev, stage или prod.
- `fallback` — запасное значение при отсутствии основной настройки.
- `configuration` — внешние настройки программы.
- `duplicate test` — повторная копия уже существующего теста.

## Правило дня

Адрес стенда хранится в конфигурации, а не размножается по fixtures и тестам.
