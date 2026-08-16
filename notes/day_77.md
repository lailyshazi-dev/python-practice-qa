# День 77: отдельные CI jobs и зависимость needs

## Цель урока

Разделить smoke- и regression-проверки на отдельные GitHub Actions jobs и связать их зависимостью `needs`.

## Steps и jobs

`step` — отдельная операция внутри job: загрузка репозитория, установка Python, установка зависимостей или запуск pytest.

Все steps одного job:

- выполняются последовательно;
- используют одну виртуальную машину;
- видят общий рабочий каталог;
- используют установленные предыдущими шагами программы.

`job` — отдельная задача pipeline. Каждый job по умолчанию получает новую изолированную виртуальную машину.

Поэтому второй job не наследует:

- файлы первого job;
- установленное виртуальное окружение;
- Chromium;
- переменные, созданные только внутри первого job.

Именно поэтому в smoke и regression повторяются checkout, установка Python, зависимостей и браузера Playwright.

## Smoke job

```yaml
jobs:
  smoke:
    name: Smoke tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
```

Smoke job запускает только критические тесты:

```yaml
python -m pytest -m smoke
```

Его результаты сохраняются отдельно:

```text
smoke-test-artifacts
reports/smoke-report.html
reports/smoke-junit.xml
```

## Regression job

```yaml
  regression:
    name: Regression tests
    needs: smoke
```

`needs: smoke` создаёт зависимость. Regression запускается только после успешного завершения smoke.

Последовательность pipeline:

```text
Smoke tests passed
        |
        v
Regression tests started
```

Если smoke падает, regression получает статус skipped. Это экономит время runner и быстро сообщает, что сборка не прошла базовую проверку.

## Исключение повторного запуска

Smoke-тесты уже выполнены первым job, поэтому regression запускает оставшиеся тесты:

```yaml
python -m pytest -m "not smoke"
```

Логическое выражение `not smoke` означает: выбрать все тесты, у которых нет маркера `smoke`.

Таким образом:

```text
smoke tests + not smoke tests = all tests
```

Локальный полный запуск по-прежнему выполняется обычной командой:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Артефакты из разных jobs

Каждый job публикует собственный архив:

```text
smoke-test-artifacts
regression-test-artifacts
```

Одинаковые имена артефактов могли бы вызвать конфликт. Разные имена также помогают сразу понять, к какому этапу относится отчёт.

Если второму job понадобятся реальные файлы первого, их нужно передать явно через `actions/upload-artifact` и `actions/download-artifact`. `needs` управляет порядком и статусом, но само по себе файлы не передаёт.

## Реальные примеры

### Pipeline перед релизом

Smoke проверяет авторизацию, открытие каталога и создание заказа. Только после успеха запускаются сотни регрессионных тестов оплаты, фильтров, ролей и ошибок API.

### Сборка приложения

Job `build` создаёт установочный пакет и загружает его как artifact. Job `test` использует `needs: build`, скачивает artifact и тестирует именно собранную версию.

### Deployment

Job `deploy` зависит от тестовых jobs. Если хотя бы обязательная проверка упала, deployment не начинается.

## Реальная ошибка с Git-веткой

Коммит `977b94f` сначала был создан в `master`, потому что команда создания feature-ветки не была выполнена. Git всегда записывает новый коммит в текущую активную ветку.

Файлы сами по себе не принадлежат ветке. Ветка — это подвижный указатель на коммит, а `HEAD` показывает текущую ветку.

Перед началом работы полезно проверять:

```powershell
git branch --show-current
git status --short --branch
```

Коммит был безопасно сохранён в `refactor/split-ci-jobs`, локальный `master` возвращён к `origin/master`, после чего ветка объединена обычным merge-коммитом.

Итоговая история:

```text
977b94f  Split smoke and regression CI jobs
62e8829  Merge smoke and regression CI jobs
```

## Результат

```text
smoke и regression разделены на jobs
regression зависит от smoke через needs
тесты разделены выражением not smoke
создаются два набора артефактов
master и origin/master синхронизированы
git diff --check без ошибок
```

## Правило дня

Steps одного job разделяют окружение, а jobs изолированы. `needs` задаёт зависимость между jobs, но не переносит между ними файлы.

