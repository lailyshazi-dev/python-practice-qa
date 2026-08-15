# День 70: анализ Playwright Trace

## Цель урока

Научиться читать trace-файл и отличать действия теста, locators, загрузку страницы и сетевые запросы приложения.

## Trace-файл

Trace был создан для теста:

```text
C:\Users\Admin\Documents\qa_automation_course\python-practice-qa\test-results\tests-ui-test-todo-page-py-test-user-can-add-todo-chromium-locators\trace.zip
```

Trace-файлы находятся в `test-results` и не должны добавляться в Git: это временные диагностические артефакты.

## Что показал trace

В trace обнаружено 7 основных действий:

1. Создание новой страницы.
2. Переход на TodoMVC.
3. Заполнение поля задачи.
4. Нажатие `Enter`.
5. Проверка видимости названия.
6. Проверка количества задач.
7. Проверка текста `1 item left`.

Количество действий совпало с наблюдением в Trace Viewer.

## Locator поля задачи

В trace виден вызов:

```text
get_by_placeholder("What needs to be done?")
```

Внутренне Playwright использует locator по атрибуту `placeholder`:

```html
<input placeholder="What needs to be done?">
```

Поэтому `/todomvc/` не является locator. Это path части URL:

```text
https://demo.playwright.dev/todomvc/
```

Другие locators этого теста:

- `get_by_text("Learn Playwright locators", exact=True)`;
- `get_by_test_id("todo-item")`;
- `get_by_text("1 item left", exact=True)`.

## Сетевой запрос

В trace есть:

```text
GET https://demo.playwright.dev/todomvc/
```

Это запрос загрузки HTML-страницы. Также браузер загружает CSS и JavaScript.

Отдельного `POST`, `PUT` или `PATCH` после добавления задачи нет. Demo TodoMVC создаёт задачу в клиентском состоянии приложения, поэтому действие не отправляет её на backend.

В реальном приложении после нажатия `Add task` мог бы появиться запрос:

```text
POST /api/tasks
```

Тогда во вкладке Network можно было бы проверить request payload, status code и response body.

## Как отличать UI-действие от network-операции

Нажатие кнопки или `press("Enter")` — это действие браузера. Оно может изменить DOM локально или вызвать сетевой запрос.

Нельзя автоматически считать, что каждое изменение UI отправляет данные на сервер. Это проверяется во вкладке Network или через `page.expect_request()`.

## Пример для реального приложения

Для формы заказа тест может выполнить:

```text
заполнить форму
нажать Submit
проверить POST /api/orders
проверить status 201
проверить страницу подтверждения
```

Если UI изменился, но POST не отправился, возможны проблемы JavaScript, валидации или обработки кнопки.

## Что смотреть в Trace Viewer

- **Actions** — последовательность шагов;
- **Call** — locator, параметры и длительность;
- **Before / Action / After** — DOM до и после;
- **Network** — запросы и ответы;
- **Console** — сообщения и JavaScript errors;
- **Metadata** — браузер, viewport и длительность.

## Результат урока

Trace помог подтвердить, что locator поля устойчиво основан на placeholder, страница загружается через GET, а добавление задачи в demo-приложении происходит без backend-запроса.

## Правило дня

URL, locator и network request — разные понятия: URL открывает ресурс, locator находит элемент, request обменивается данными с сервером.

## Источник

Официальная документация Playwright Trace Viewer: https://playwright.dev/python/docs/trace-viewer
