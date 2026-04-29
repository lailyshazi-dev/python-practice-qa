# День 13: HTML-отчет pytest

## Что я сделал

- Установил плагин `pytest-html`.
- Обновил файл `requirements.txt`.
- Запустил тесты с генерацией HTML-отчета.
- Получил отчет в папке `reports/`.
- Убедился, что все тесты проходят.

## Что понял

- `pytest-html` добавляет к pytest возможность создавать отчет в формате HTML.
- HTML-отчет удобно открывать в браузере.
- В отчете видно, какие тесты прошли, упали или были пропущены.
- Такой отчет полезен для QA, потому что его можно показать команде или приложить к результатам проверки.
- Флаг `--self-contained-html` делает отчет одним HTML-файлом, без отдельных CSS и JS файлов.

## Команды дня

```powershell
.\.venv\Scripts\python.exe -m pip install pytest-html
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
.\.venv\Scripts\python.exe -m pytest --html=reports/report.html --self-contained-html
```

## Результат

```text
34 passed
Generated html report: reports/report.html
```

## Новые слова

- `report` - отчет.
- `HTML report` - отчет в формате HTML.
- `plugin` - расширение для программы.
- `self-contained` - самостоятельный файл, которому не нужны дополнительные файлы рядом.
- `generated file` - файл, который создается автоматически командой.

## Правило дня

Отчет не заменяет тесты, а помогает удобно показать результат их запуска.

