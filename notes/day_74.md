# День 74: GitHub Actions CI для автотестов

## Цель урока

Подключить GitHub Actions, чтобы тесты проекта автоматически запускались на сервере после изменений в `master` и при Pull Request.

## Что такое CI

CI (Continuous Integration, непрерывная интеграция) — автоматическая проверка изменений после отправки кода в удалённый репозиторий.

Вместо того чтобы каждый раз вручную устанавливать зависимости и запускать тесты на своём компьютере, GitHub Actions создаёт чистую виртуальную машину и повторяет проверку по сценарию из workflow.

## Файл workflow

Workflow создан в файле `.github/workflows/tests.yml`. GitHub распознаёт YAML-файлы внутри каталога `.github/workflows` и показывает их во вкладке **Actions**.

Основные части workflow:

```yaml
name: QA tests

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
```

Здесь указано, что проверка запускается:

- после `push` в ветку `master`;
- при Pull Request, направленном в `master`.

Это полезно для защиты основной ветки: изменения сначала проходят автоматические проверки, а уже потом объединяются с `master`.

## Последовательность CI-проверки

### 1. Checkout

```yaml
- name: Checkout repository
  uses: actions/checkout@v6
```

Шаг загружает содержимое репозитория на виртуальную машину GitHub Actions.

### 2. Установка Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v6
  with:
    python-version: "3.12"
    cache: pip
```

CI использует ту же версию Python, что и локальный проект. Кэш pip ускоряет повторные запуски, потому что зависимости не всегда приходится скачивать заново.

### 3. Установка зависимостей

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
```

Файл `requirements.txt` становится единым источником зависимостей для разработчика и CI-сервера. Это уменьшает риск ситуации «у меня работает, а на сервере нет».

### 4. Установка браузера Playwright

```yaml
- name: Install Playwright browsers
  run: |
    python -m playwright install --with-deps chromium
```

Одной установки Python-пакета Playwright недостаточно: для UI-тестов нужен браузер Chromium и его системные зависимости.

### 5. Запуск тестов

```yaml
- name: Run tests
  run: |
    python -m pytest \
      --html=reports/report.html \
      --self-contained-html
```

Если хотя бы один тест завершается с ошибкой, шаг получает ненулевой код завершения, а workflow помечается как failed.

### 6. Сохранение артефактов

```yaml
- name: Upload test artifacts
  if: ${{ !cancelled() }}
  uses: actions/upload-artifact@v5
  with:
    name: qa-test-artifacts
    path: |
      reports/
      test-results/
```

Артефакты позволяют скачать HTML-отчёт pytest, trace Playwright, скриншоты и другие файлы после завершения запуска.

## Реальные примеры применения

### Pull Request

QA-инженер или разработчик создаёт Pull Request. GitHub Actions запускает тесты до code review. Если сломался UI-тест или API-проверка, команда видит проблему до попадания изменений в `master`.

### Ночная регрессия

В рабочем проекте workflow можно запускать по расписанию. Утром команда получает результат полной регрессии и может сразу открыть отчёт или Playwright trace.

### Подготовка релиза

Перед публикацией версии CI проверяет критический smoke-набор. Если smoke-тесты не проходят, релиз блокируется до исправления проблемы.

## Важная ошибка текущего урока

Сначала workflow был отправлен только в feature-ветку. Но в конфигурации `push` разрешён лишь для `master`, поэтому отправка feature-ветки не запустила проверку.

После объединения feature-ветки в `master` и выполнения:

```text
git push origin master
```

GitHub обнаружил workflow и создал первый запуск.

## Результат

```text
1 workflow run
master и origin/master синхронизированы
рабочее дерево чистое
```

## Правило дня

Workflow должен находиться в репозитории и иметь подходящий trigger. Наличие файла в локальной feature-ветке ещё не означает, что GitHub уже запустит CI для `master`.

