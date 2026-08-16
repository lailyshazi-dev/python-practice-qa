# День 75: диагностика GitHub Actions и JUnit-отчёт

## Цель урока

Научиться находить причину падения workflow и сохранять результаты pytest в стандартном формате JUnit XML.

## Как читать workflow

Красный статус всего workflow сообщает только о том, что один из шагов завершился ошибкой. Для диагностики нужно открыть конкретный failed step и прочитать его лог.

Основные шаги нашего pipeline:

- `Checkout repository` загружает код;
- `Set up Python` подготавливает версию Python;
- `Install dependencies` ставит пакеты;
- `Install Playwright browsers` устанавливает Chromium;
- `Run tests` выполняет pytest;
- `Upload test artifacts` сохраняет отчёты и trace.

Если ошибка произошла на `Run tests`, сначала проверяем название теста, traceback и последнюю строку с итогом pytest. Если проблема связана с Playwright, дополнительно скачиваем trace или screenshot из Artifacts.

## JUnit XML

В шаг запуска тестов добавлен параметр:

```yaml
python -m pytest \
  --html=reports/report.html \
  --self-contained-html \
  --junitxml=reports/junit.xml
```

`junit.xml` содержит машинно-читаемые результаты: количество тестов, ошибки, failures и время выполнения. Такой формат понимают Jenkins, GitLab CI, TeamCity и другие CI-системы.

HTML-отчёт удобен для ручного анализа, а JUnit XML — для автоматической обработки и отображения статистики в интерфейсе CI.

## Важная синтаксическая ошибка

В YAML-команде используется многострочный shell-блок. Обратная косая черта в конце строки означает, что следующая строка продолжает ту же команду.

Неправильно:

```yaml
--self-contained-html
--junitxml=reports/junit.xml
```

В этом случае shell пытается запустить `--junitxml=reports/junit.xml` как отдельную команду.

Правильно:

```yaml
--self-contained-html \
--junitxml=reports/junit.xml
```

После исправления workflow прошёл проверку, а `master` и `origin/master` синхронизированы на merge-коммите `929734f`.

## Артефакты

В Actions нужно открыть конкретный run и найти раздел **Artifacts**. Архив `qa-test-artifacts` должен содержать:

- `reports/report.html`;
- `reports/junit.xml`;
- файлы из `test-results/`, если Playwright создал trace или screenshot.

Артефакты особенно важны, когда ошибка воспроизводится только на Linux runner или только в CI.

## Реальные примеры

### Падение UI-теста

В логах видно, что locator не найден. Screenshot показывает состояние страницы, а trace позволяет открыть последовательность действий и увидеть, после какого шага интерфейс изменился.

### Ошибка зависимостей

Если падает `Install dependencies`, проверяем `requirements.txt`, совместимость версий и сообщение pip. До запуска тестов проблема относится не к тестовой логике, а к окружению.

### Отчёт для команды

JUnit XML можно подключить к dashboard CI. QA-команда видит число passed, failed и skipped без ручного открытия каждого лога.

## Результат проверки

```text
workflow успешно запущен
JUnit XML добавлен
master и origin/master синхронизированы
git diff --check без ошибок
```

## Правило дня

При диагностике CI сначала определяем упавший шаг, затем читаем его лог, после этого скачиваем подходящий артефакт. Нельзя делать вывод о причине только по красному значку workflow.
