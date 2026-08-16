# День 80: ручной и запланированный запуск GitHub Actions

## Цель урока

Добавить ручной выбор тестового набора, запуск по расписанию и корректную обработку skipped jobs.

## События workflow

Workflow поддерживает четыре способа запуска:

```yaml
on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
  workflow_dispatch:
  schedule:
```

### Push

Запускается после отправки коммита в `master`. Используется для проверки уже объединённых изменений.

### Pull request

Запускается для изменений, которые предлагают объединить с `master`. Позволяет обнаружить проблему до merge.

### Workflow dispatch

Создаёт кнопку **Run workflow** и позволяет вручную выбрать параметры запуска.

### Schedule

Запускает workflow по расписанию cron. В проекте полный pipeline запускается каждый понедельник в `03:00 UTC`:

```yaml
schedule:
  - cron: "0 3 * * 1"
```

GitHub Actions использует UTC, а scheduled workflow берётся из основной ветки репозитория.

## Ручной выбор набора

```yaml
workflow_dispatch:
  inputs:
    suite:
      description: Test suite to run
      required: true
      default: all
      type: choice
      options:
        - all
        - smoke
        - regression
        - ui
```

После merge этого блока в `master` на странице конкретного workflow появилась кнопка **Run workflow**.

Кнопка может отсутствовать, если:

- `workflow_dispatch` существует только в feature-ветке;
- открыта страница `All workflows`, а не конкретный `QA tests`;
- пользователь не авторизован или не имеет права записи.

## Условия jobs

Smoke запускается всегда как обязательный gate.

Regression выполняется для обычных событий, а при ручном запуске — только для `all` или `regression`:

```yaml
if: ${{ github.event_name != 'workflow_dispatch' || inputs.suite == 'all' || inputs.suite == 'regression' }}
```

Browser matrix выполняется для обычных событий, а при ручном запуске — только для `all` или `ui`:

```yaml
if: ${{ github.event_name != 'workflow_dispatch' || inputs.suite == 'all' || inputs.suite == 'ui' }}
```

## Работа со skipped jobs

Job `report` зависит от smoke, regression и UI matrix. При выборе только smoke два зависимых job получают статус `skipped`.

Чтобы collector всё равно запустился, добавлено условие:

```yaml
if: ${{ always() && !cancelled() && needs.smoke.result == 'success' }}
```

Значение частей выражения:

- `always()` разрешает оценить job после failed или skipped dependencies;
- `!cancelled()` не запускает collector после отмены workflow;
- `needs.smoke.result == 'success'` требует успешного критического gate.

## Условное скачивание

Artifact скачивается только тогда, когда соответствующий job действительно прошёл:

```yaml
if: ${{ needs.regression.result == 'success' }}
```

```yaml
if: ${{ needs.ui_matrix.result == 'success' }}
```

Без этих условий ручной smoke-запуск попытался бы скачать несуществующие regression- и UI-архивы.

## Реальные сценарии

### Hotfix

После небольшого срочного исправления QA вручную запускает `smoke` и быстро проверяет критические функции.

### Изменение интерфейса

QA выбирает `ui`, поэтому после smoke выполняется browser matrix, но API/calculator regression не расходует время runner.

### Релиз

Перед релизом выбирается `all`: smoke, regression, Chromium, Firefox, WebKit и collector.

### Регулярная проверка

Schedule запускает полный pipeline без ручного участия и помогает обнаружить проблемы внешних сервисов или окружения.

## Проверка урока

Полный запуск после merge выполнил весь pipeline. Затем вручную был выбран `smoke`.

Полученный граф:

```text
Smoke tests              passed
Regression tests         skipped
UI tests                 skipped
Collect test reports     passed
```

Это подтверждает, что input, job conditions и условное скачивание artifacts работают согласованно.

## Обнаруженное предупреждение

GitHub сообщил, что `actions/upload-artifact@v5` использует устаревающую среду Node.js 20 и принудительно переводится на Node.js 24. Тесты не упали, но предупреждение показывает технический долг зависимости workflow. Обновление actions будет выполнено отдельным уроком.

## Результат

```text
Run workflow доступен
ручной smoke прошёл
ненужные jobs получили skipped
collector прошёл
еженедельный schedule добавлен
master и origin/master синхронизированы
```

## Правило дня

Событие определяет, когда запускается workflow, input — что выбрал пользователь, а job-level `if` — какие части pipeline действительно должны выполняться.

