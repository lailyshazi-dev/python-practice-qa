# День 85: Page Object для Selenium

02.09.2026 · Блок 0 · Связи: day_83, day_84, tests/ui/pages/todo_page.py (Playwright PO) · Банк: №17

## Зачем

Тест должен читаться как сценарий пользователя, а не как набор локаторов и ожиданий. Page Object прячет «как найти и дождаться» в класс страницы; тест знает только «что сделать». На собеседовании это вопрос №17 банка и первое, что спрашивают про UI-автотесты.

## Предпосылки

- day_83: фикстура `selenium_driver`, явные ожидания.
- day_84: константы-локаторы, фикстура `wait`, сообщения в `until()`.

## Ход

**Шаг 1. Класс страницы.** Предскажи: куда переедут `By.` и `EC.` из теста? Файл `tests/selenium/pages/todo_page.py`:

```python
class SeleniumTodoPage:
    TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_ITEM = (By.CSS_SELECTOR, ".todo-list li")
    TODO_LABEL = (By.CSS_SELECTOR, ".todo-list li label")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    TODO_TOGGLE = (By.CSS_SELECTOR, ".todo-list li .toggle")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, url):
        self.driver.get(url)

    def add_todo(self, title):
        todo_input = self.wait.until(
            EC.visibility_of_element_located(self.TODO_INPUT),
            "Todo input did not appear",
        )
        todo_input.send_keys(title, Keys.ENTER)

    def wait_items_left(self, text):
        self.wait.until(
            EC.text_to_be_present_in_element(self.TODO_COUNT, text),
            f"Counter did not show '{text}'",
        )

    def visible_todos(self):
        return self.driver.find_elements(*self.TODO_ITEM)
```

Ещё четыре метода по той же схеме: `first_todo_title`, `complete_first_todo` (ждёт presence — day_84), `clear_completed`, `wait_list_empty`. `wait` и `driver` приходят один раз в конструктор, методы берут их из `self`.

**Шаг 2. Фикстура.** В `tests/selenium/conftest.py`:

```python
@pytest.fixture
def todo_page(selenium_driver, wait):
    return SeleniumTodoPage(selenium_driver, wait)
```

**Шаг 3. Тест без единого `By.` и `EC.`:**

```python
pytestmark = pytest.mark.selenium

def test_user_can_complete_and_clear_todo(todo_page, base_url):
    todo_page.open(base_url)
    todo_page.add_todo("Learn explicit waits")
    todo_page.wait_items_left("1 item left")
    todo_page.complete_first_todo()
    todo_page.wait_items_left("0 items left")
    todo_page.clear_completed()
    todo_page.wait_list_empty()
    assert todo_page.visible_todos() == []
```

**Шаг 4. Запуск.** Предскажи итог: `pytest -m selenium` → `2 passed, 111 deselected` (113 тестов в проекте). Увидели: так и есть, 22 с.

**Шаг 5. `pythonpath = .` в pytest.ini.** Раньше голый `pytest` падал с `ModuleNotFoundError: src`, а `python -m pytest` работал: `-m` добавляет текущую папку в пути поиска, скрипт `pytest` — нет. Теперь pytest сам добавляет корень проекта, и на чистом клоне работает любая команда.

## Ошибка дня: папка заслонила библиотеку

Симптом: `ImportError: cannot import name 'webdriver' from 'selenium' (...tests\selenium\__init__.py)`. Как нашли: путь в скобках — наша папка, не site-packages. Причина: добавили `tests/selenium/__init__.py` → папка стала пакетом с именем `selenium` и перекрыла библиотеку (name shadowing). Фикс: `tests/__init__.py` — пакет стал `tests.selenium`. Чего не делать: называть свои папки и файлы именами библиотек (`selenium/`, `requests.py`).

## Результат (02.09 написал наставник; ученик пересказывает своими словами 03.09)

В проекте появился класс `SeleniumTodoPage` в `tests/selenium/pages/todo_page.py`: шесть локаторов и восемь методов-действий с ожиданиями и сообщениями внутри. Тесты сократились с 74 до 28 строк и читаются как сценарий. В `pytest.ini` добавлен `pythonpath = .`, папка `tests` стала пакетом.

## Правило дня (02.09 написал наставник; ученик формулирует сам 03.09)

Локаторы и ожидания живут в классе страницы, тесты знают только методы. Меняется вёрстка — правится один файл.

## Карточка для тетради

```text
D85 · 02.09 · Page Object для Selenium
ЗАЧЕМ: тест = сценарий, страница = класс
ЯДРО:
 - локаторы = атрибуты класса (кортежи), действия = методы
 - driver и wait один раз в __init__, дальше self.wait / self.driver
 - фикстура todo_page собирает страницу из selenium_driver + wait
 - тест: open → add_todo → wait_items_left → ... → assert; ни одного By./EC.
 - pythonpath = . : голый pytest работает как python -m pytest
ОШИБКА ДНЯ: папка tests/selenium стала пакетом selenium → заслонила библиотеку → tests/__init__.py
ПРАВИЛО: вёрстка меняется — правим один файл, тесты не трогаем
ВОПРОС СЕБЕ: почему wait в конструкторе, а не параметром каждого метода?
```

## Второй проход (фаза 2) — сделай сам с клавиатурой

Исходное состояние: репозиторий v2, `tests/selenium/conftest.py` с фикстурами `selenium_driver` и `wait`, пустой `tests/selenium/pages/todo_page.py`, два теста из day_84 с локаторами в модуле.
Сделать: 1) класс `SeleniumTodoPage` с 6 локаторами и 8 методами (`open`, `add_todo`, `first_todo_title`, `complete_first_todo`, `clear_completed`, `wait_items_left`, `wait_list_empty`, `visible_todos`); 2) фикстура `todo_page`; 3) переписать оба теста на методы страницы; 4) `pytestmark`; 5) `pythonpath = .`. Время: 60 мин.
Готово, когда: `pytest -m selenium` → 2 passed; в тесте нет `By.`/`EC.`; каждый `until` с сообщением; нет `sleep`/`implicitly_wait`; коммит в feature-ветке через PR.
Если застрял: подсказка 1 → раздел «Ход» · подсказка 2 → карточка D85 · только потом код v1 (правило 20 минут).

## Самопроверка

1. Зачем `wait` передаётся в конструктор один раз, а не в каждый метод?
   <details>Страница владеет своим ожиданием: один таймаут для всех действий, методы короче, тест не знает про WebDriverWait вообще. Поменять таймаут — одна строка в conftest.</details>
2. Переименовали класс `.new-todo` на сайте. Сколько файлов править?
   <details>Один — `pages/todo_page.py`, константа `TODO_INPUT`. Тесты не трогаем.</details>
3. Как это спросят на собеседовании: «Что такое Page Object и зачем он?»
   <details>Паттерн: страница — класс, локаторы — его поля, действия пользователя — методы; тесты работают только с методами. Даёт читаемость тестов, одну точку правки при изменении вёрстки, переиспользование действий. Пример: SeleniumTodoPage в моём проекте.</details>
