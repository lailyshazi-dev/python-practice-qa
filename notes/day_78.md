# День 78: передача артефактов между CI jobs

## Цель урока

Научиться передавать файлы между изолированными GitHub Actions jobs и собирать единый архив тестовых отчётов.

## Итоговый pipeline

Workflow состоит из трёх последовательных jobs:

```text
Smoke tests
     |
     v
Regression tests
     |
     v
Collect test reports
```

Job `report` зависит от двух тестовых jobs:

```yaml
  report:
    name: Collect test reports
    needs:
      - smoke
      - regression
```

По умолчанию он запускается только после их успешного завершения.

## Почему needs недостаточно

`needs` управляет порядком и статусами jobs, но не переносит файлы. Каждый job запускается на отдельной виртуальной машине со своей файловой системой.

Для передачи файлов используется цепочка:

```text
upload-artifact
       |
       v
хранилище GitHub Actions
       |
       v
download-artifact
```

Smoke и regression сначала публикуют отдельные архивы:

```text
smoke-test-artifacts
regression-test-artifacts
```

## Скачивание артефактов

Job `report` скачивает каждый архив в отдельный каталог:

```yaml
      - name: Download smoke artifacts
        uses: actions/download-artifact@v5
        with:
          name: smoke-test-artifacts
          path: collected-artifacts/smoke
```

```yaml
      - name: Download regression artifacts
        uses: actions/download-artifact@v5
        with:
          name: regression-test-artifacts
          path: collected-artifacts/regression
```

Разные каталоги не позволяют одинаковым именам файлов перезаписать друг друга.

## Диагностический шаг

```yaml
      - name: Show collected files
        run: |
          find collected-artifacts -type f -print
```

Команда выводит в лог список скачанных файлов. Это позволяет проверить не только успешный статус action, но и фактическое содержимое каталогов.

## Общий архив

После скачивания создаётся итоговый artifact:

```yaml
      - name: Upload combined artifacts
        uses: actions/upload-artifact@v5
        with:
          name: combined-test-artifacts
          path: collected-artifacts/
          if-no-files-found: error
          retention-days: 14
```

`if-no-files-found: error` делает отсутствие файлов явной ошибкой. Без этого pipeline мог бы стать зелёным, даже если отчёты фактически не были собраны.

## Artifact и cache

Artifact хранит результат конкретного запуска:

- HTML- или JUnit-отчёт;
- Playwright trace;
- screenshot или video;
- собранное приложение;
- логи диагностики.

Cache предназначен для ускорения следующих запусков:

- пакеты pip;
- npm dependencies;
- загруженные инструменты;
- промежуточные файлы сборки.

Artifact является результатом или доказательством выполнения job. Cache является оптимизацией и может отсутствовать, устареть или не совпасть по ключу.

## Реальные примеры

### Отчёт перед релизом

QA скачивает один `combined-test-artifacts`, содержащий smoke- и regression-отчёты, traces и screenshots.

### Передача сборки

Job `build` публикует установочный пакет как artifact. Зависимые jobs скачивают и тестируют одну и ту же сборку.

### Ускорение установки

Cache pip сокращает время установки зависимостей, но его удаление не должно менять результат тестирования — pipeline просто выполнится дольше.

## Ошибка с YAML-отступом

Сначала `report` имел четыре пробела и оказался вложен в `regression`. Для отдельного job перед его именем должны быть два пробела, как у `smoke` и `regression`:

```yaml
jobs:
  smoke:
  regression:
  report:
```

`git diff --check` проверяет пробелы в конце строк и конфликты форматирования, но не понимает логическую структуру YAML. Поэтому workflow дополнительно проверяется запуском GitHub Actions.

## Результат

```text
три CI jobs успешно прошли
артефакты скачиваются между jobs
создаётся combined-test-artifacts
master и origin/master синхронизированы
git diff --check без ошибок
```

## Правило дня

Для порядка выполнения jobs используется `needs`, а для передачи файлов — artifacts. Cache предназначен для ускорения и не заменяет сохранение результатов тестирования.

