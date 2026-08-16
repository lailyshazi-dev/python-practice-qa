# День 79: Playwright browser matrix в GitHub Actions

## Цель урока

Запустить один набор UI-тестов в Chromium, Firefox и WebKit с помощью matrix strategy и собрать отдельные отчёты каждого браузера.

## Зачем нужны разные браузеры

Браузеры используют разные движки:

- Chromium — Blink;
- Firefox — Gecko;
- WebKit — движок, близкий к используемому Safari.

Одинаковая страница может по-разному обрабатывать CSS, JavaScript, формы, сетевые запросы и события. Успех теста в Chromium не гарантирует такое же поведение в Firefox или WebKit.

## Matrix strategy

Вместо трёх почти одинаковых jobs описывается один шаблон:

```yaml
  ui_matrix:
    name: UI tests (${{ matrix.browser }})
    needs: smoke
    strategy:
      fail-fast: false
      matrix:
        browser:
          - chromium
          - firefox
          - webkit
```

GitHub Actions разворачивает шаблон в три отдельных запуска:

```text
UI tests (chromium)
UI tests (firefox)
UI tests (webkit)
```

Каждый вариант matrix получает отдельный runner и выполняется независимо.

## Использование параметра matrix

Текущий браузер устанавливается динамически:

```yaml
python -m playwright install --with-deps ${{ matrix.browser }}
```

Тот же параметр передаётся pytest-playwright:

```yaml
python -m pytest -m ui \
  --browser ${{ matrix.browser }}
```

Один и тот же тестовый код запускается в разных браузерах без копирования тестовых функций.

## Fail-fast

```yaml
fail-fast: false
```

Если тесты падают в одном браузере, остальные варианты matrix продолжают выполняться. QA получает полную картину совместимости, а не только результат первого упавшего браузера.

Например, если Firefox упал, но Chromium и WebKit прошли, это важный сигнал о браузерно-зависимом дефекте.

## Разделение наборов

Обычный regression job больше не запускает UI-тесты:

```yaml
python -m pytest -m "not smoke and not ui"
```

Поэтому ему не требуется установка браузера Playwright. Это сокращает время и расход ресурсов runner.

UI-набор выполняется отдельно:

```yaml
python -m pytest -m ui
```

Критические UI smoke-тесты намеренно запускаются сначала в Chromium как быстрый gate, а затем ещё раз в browser matrix для проверки совместимости.

## Отдельные артефакты

Имя браузера включено в имя artifact:

```yaml
name: ui-${{ matrix.browser }}-test-artifacts
```

Создаются три архива:

```text
ui-chromium-test-artifacts
ui-firefox-test-artifacts
ui-webkit-test-artifacts
```

Job `report` зависит от всей matrix:

```yaml
needs:
  - smoke
  - regression
  - ui_matrix
```

После завершения matrix он скачивает отчёты каждого браузера в отдельные каталоги и добавляет их в `combined-test-artifacts`.

## Итоговый граф

```text
Smoke tests
 |-- Regression tests
 |-- UI tests (chromium)
 |-- UI tests (firefox)
 `-- UI tests (webkit)
              |
              v
     Collect test reports
```

## Реальные примеры применения

### Интернет-магазин

Оформление заказа работает в Chromium, но в WebKit кнопка перекрыта другим элементом. Cross-browser UI-тест обнаруживает проблему до релиза для пользователей Safari.

### Корпоративная система

Большинство сотрудников использует Chromium, но часть работает в Firefox. Matrix подтверждает поддержку обоих браузеров одним тестовым набором.

### Диагностика

Если падает только один вариант matrix, QA сравнивает его trace, screenshot и сетевые события с успешными браузерами.

## Ошибки урока

Были исправлены четыре проблемы YAML:

- `ui_matrix` сначала оказался вложен в `regression`;
- в `- ui_matrix` отсутствовал пробел;
- шаг Chromium имел лишний отступ;
- regression сначала не исключал маркер `ui`.

Также исправления сначала не попали в Git, потому что файл был изменён в редакторе, но не сохранён.

Перед коммитом полезно выполнять:

```powershell
git status --short
git diff -- .github/workflows/tests.yml
```

Если Git не показывает `M` и diff пустой, сохранённого изменения нет.

## Результат

```text
Chromium прошёл
Firefox прошёл
WebKit прошёл
Collect test reports прошёл
master и origin/master синхронизированы
git diff --check без ошибок
```

## Правило дня

Matrix устраняет копирование одинаковых jobs, а `fail-fast: false` позволяет получить результаты всех вариантов даже при браузерно-зависимом падении.

