# День 62: первые UI-тесты на Playwright

## Что я сделал

- Создал ветку `feature/add-first-playwright-tests`.
- Установил `pytest-playwright` и совместимый Chromium.
- Закрепил новые зависимости в `requirements.txt`.
- Добавил pytest marker `ui`.
- Создал каталог `tests/ui`.
- Написал первые два браузерных теста.
- Проверил title страницы и видимость heading.
- Запустил UI-набор отдельно и весь проект.

## Что такое Playwright

Playwright — инструмент автоматизации современных браузеров. Python-код может:

- открывать страницы;
- находить элементы;
- вводить текст;
- нажимать кнопки и ссылки;
- проверять URL, title, текст и состояние элементов;
- работать с вкладками, cookies, загрузками и сетевыми запросами;
- запускать Chromium, Firefox и WebKit.

В проекте используется официальный pytest-плагин. Он предоставляет готовые fixtures, включая `page`.

## Установка

```powershell
.\.venv\Scripts\python.exe -m pip install pytest-playwright
.\.venv\Scripts\python.exe -m playwright install chromium
```

Первая команда устанавливает Python-пакеты. Вторая загружает браузерные binaries, совместимые с версией Playwright.

Одной записи пакета в `requirements.txt` недостаточно для новой машины или CI: после установки зависимостей нужно отдельно выполнить установку браузера.

## Закреплённые зависимости

```text
greenlet==3.5.4
playwright==1.61.0
pyee==13.0.1
pytest-base-url==2.1.0
pytest-playwright==0.8.0
python-slugify==8.0.4
text-unidecode==1.3
typing_extensions==4.16.0
```

Часть пакетов установлена как транзитивные зависимости плагина. Их фиксация делает восстановление учебного окружения воспроизводимым.

## Структура UI-тестов

```text
tests/
└── ui/
    └── test_example_page.py
```

API- и UI-тесты разделены по каталогам, потому что у них разные зависимости, скорость, причины падений и способы диагностики.

## Marker

```ini
markers =
    ui: browser user interface test
```

В файле тестов:

```python
pytestmark = pytest.mark.ui
```

Это помечает все тесты модуля. Только UI-набор запускается командой:

```powershell
.\.venv\Scripts\python.exe -m pytest -m ui
```

## Первый тест: title страницы

```python
def test_example_page_has_expected_title(page: Page):
    page.goto(EXAMPLE_URL)

    expect(page).to_have_title("Example Domain")
```

- `page` создаётся pytest-плагином.
- `page.goto()` открывает URL.
- `expect(page).to_have_title()` проверяет title документа.
- После теста изолированный browser context очищается автоматически.

## Второй тест: locator и heading

```python
def test_example_page_has_visible_heading(page: Page):
    page.goto(EXAMPLE_URL)

    heading = page.get_by_role(
        "heading",
        name="Example Domain",
    )

    expect(heading).to_be_visible()
```

`get_by_role()` ищет элемент по роли и accessible name. Такой locator описывает намерение пользователя лучше, чем хрупкая привязка к CSS-структуре.

Например:

```python
page.get_by_role("button", name="Sign in")
page.get_by_label("Email")
page.get_by_text("Welcome")
```

## Web-first assertion

```python
expect(heading).to_be_visible()
```

Playwright некоторое время повторно проверяет условие. Это помогает при динамической загрузке страницы.

Не следует сразу писать:

```python
time.sleep(5)
```

Фиксированная пауза всегда ждёт полное время и всё равно может оказаться слишком короткой. Locator и `expect()` ожидают конкретное состояние.

## Headless и headed

По умолчанию тесты запускаются в headless-режиме: окно браузера не показывается. Это быстрее и удобно для CI.

Чтобы увидеть выполнение:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_example_page.py --headed --slowmo 500
```

- `--headed` показывает окно браузера;
- `--slowmo 500` замедляет действия для наблюдения и обучения.

Slow motion используют для диагностики, но не оставляют обязательным режимом обычного CI-прогона.

## Где это нужно в реальной работе

- Проверка регистрации и авторизации через браузер.
- Добавление товара в корзину и переход к checkout.
- Заполнение форм и проверка сообщений валидации.
- Проверка ролей пользователя в интерфейсе.
- Загрузка и скачивание файлов.
- Проверка критического smoke-сценария после deployment.
- Cross-browser проверка в Chromium, Firefox и WebKit.

Например, API-тест быстро проверит десятки вариантов корзины, а Playwright проверит один критический путь пользователя: открыть товар, добавить его, увидеть правильную сумму и перейти к оформлению.

## Ограничение текущих тестов

Тесты открывают внешний `https://example.com`. Поэтому они могут упасть из-за отсутствия интернета, DNS или недоступности сайта, даже если тестовый код правильный.

Это первые учебные UI-тесты. Дальше мы перейдём на предназначенный для практики сайт, добавим fixtures, base URL, действия пользователя и Page Object Model.

## Результат

```text
No broken requirements found
2 passed, 98 deselected — UI marker
100 passed — весь проект
git diff --check без ошибок
```

## Новые слова

- `browser automation` — управление браузером из кода.
- `page fixture` — готовая вкладка браузера для теста.
- `locator` — способ найти элемент на странице.
- `accessible name` — доступное имя элемента.
- `web-first assertion` — проверка с автоматическим ожиданием.
- `headless` — запуск без видимого окна.
- `headed` — запуск с видимым окном.
- `browser binary` — установленный исполняемый файл браузера.

## Правило дня

Ищем элементы по устойчивому пользовательскому смыслу и ждём состояние через `expect()`, а не через фиксированный `sleep`.
