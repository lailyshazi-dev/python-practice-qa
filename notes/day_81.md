# День 81: обновление GitHub Actions и Dependabot

## Цель урока

Устранить предупреждения устаревшего Node.js runtime, безопасно обновить зависимости workflow и подключить автоматический контроль версий.

## Причина обновления

GitHub Actions показывал предупреждение для `actions/upload-artifact@v5`: action был рассчитан на Node.js 20 и принудительно выполнялся на Node.js 24.

Тесты оставались зелёными, но warning указывал на технический долг. Node.js 20 достиг конца жизненного цикла, поэтому GitHub рекомендует использовать версии actions, рассчитанные на Node.js 24.

Подавлять предупреждение переменной, разрешающей устаревший runtime, неправильно. Это временная отсрочка, а не устранение причины.

## Проверка официальных источников

Перед изменением были проверены официальные репозитории GitHub Actions и changelog.

Для текущего workflow выбраны:

```text
actions/upload-artifact@v7
actions/download-artifact@v8
```

Обновление выполнялось парой, потому что upload и download работают с одним форматом артефактов.

## Инвентаризация зависимостей

Для поиска всех использований применялась команда:

```powershell
rg -n "actions/(upload|download)-artifact@" .github
```

В workflow находились:

```text
4 использования upload-artifact
5 использований download-artifact
```

После замены проверено отсутствие старой версии:

```powershell
rg -n "artifact@v5" .github
```

Пустой вывод означает, что ни одного старого вхождения не осталось.

## Обновлённые actions

```yaml
uses: actions/upload-artifact@v7
```

```yaml
uses: actions/download-artifact@v8
```

Существующие параметры `name`, `path`, `retention-days` и `if-no-files-found` менять не потребовалось.

## Dependabot

Создан файл `.github/dependabot.yml`:

```yaml
version: 2

updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

Значение полей:

- `version: 2` — версия формата конфигурации Dependabot;
- `github-actions` — проверять зависимости workflow;
- `directory: "/"` — искать workflows в стандартном `.github/workflows`;
- `weekly` — выполнять проверку раз в неделю;
- `open-pull-requests-limit: 5` — ограничить число одновременно открытых update PR.

Dependabot не изменяет `master` напрямую. Он создаёт Pull Request, который должен пройти review и CI.

## Первый результат Dependabot

Сразу после merge были созданы два Pull Request:

```text
#1 Bump actions/setup-python from 6 to 7
#2 Bump actions/checkout from 6 to 7
```

CI обоих PR завершился успешно. Однако зелёный статус не является единственным основанием для merge: нужно прочитать описание, release notes, проверить breaking changes и оценить область влияния.

## Major tag и commit SHA

Major tag:

```yaml
uses: actions/upload-artifact@v7
```

Он удобен тем, что получает исправления внутри major-ветки `v7`.

Фиксация по SHA:

```yaml
uses: actions/upload-artifact@<полный-commit-sha>
```

SHA неизменяем и лучше защищает supply chain от неожиданного перемещения тега. Такой подход часто используется в проектах с повышенными требованиями безопасности, но требует регулярного обновления через Dependabot.

Нельзя использовать `@main` или `@latest` в стабильном pipeline, потому что содержимое зависимости может измениться без review.

## Реальные примеры

### Устаревший runtime

Action продолжает работать с warning, но после удаления старого Node.js из runner внезапно перестаёт запускаться. Плановое обновление предотвращает аварийную остановку CI.

### Breaking change

Dependabot предлагает новый major. QA изучает изменение формата artifacts, запускает pipeline и проверяет не только тесты, но и возможность скачать отчёты.

### Supply-chain контроль

В регулируемом проекте actions закрепляют SHA. Dependabot предлагает новый проверенный SHA через Pull Request, а команда видит точное изменение кода зависимости.

## Проверка после merge

GitHub Actions run `#19` подтвердил:

```text
Smoke tests passed
Regression tests passed
Chromium passed
Firefox passed
WebKit passed
Collect test reports passed
Annotations: пусто
```

Созданы шесть artifacts:

```text
smoke-test-artifacts
regression-test-artifacts
ui-chromium-test-artifacts
ui-firefox-test-artifacts
ui-webkit-test-artifacts
combined-test-artifacts
```

Предупреждения Node.js 20 исчезли.

## Правило дня

Обновление зависимости CI считается проверенным только после изучения официальных изменений, успешного pipeline и проверки реального результата action, например созданных и скачанных artifacts.

