# Автоматическая генерация аналитических отчётов (ЛЦТ 2024)

<img width="850" alt="image" src="https://github.com/MisterAndry/lct2024-rag/assets/9989672/a1d299af-2e2b-4cf1-a044-f3d6dad8e610">


## Принцип работы

### Описание полей ввода UI
1. **New source** (опциональное) - поле ввода ссылок на статьи или любое другие ресурсы, которые будут парситься, добавляться в базу знаний. Вводятся по одной.
2. **Date Range** (опциональное) - временные рамки, по которым будет строиться отчёт. Можно указать как только левую границу дат, так и обе - левую и правую. Например, нужен анализ какого-то рынка только за 2020-2023 год.
3. **Template File** (обязательное) - файл шаблона в формате docx, который будет заполняться. Как должен выглядеть файл шаблона:
   В шаблоне должен быть тайтл и блоки (Слово **Блок** обязательно). В каждом блоке обязательно должен быть хотя бы один подпункт. Пример:
<img width="586" alt="image" src="https://github.com/MisterAndry/lct2024-rag/assets/9989672/e67c7b38-8f31-45f0-804c-c9c1c7f7a134">


4. **Your data files** (опциональное) - пользовательские файлы в формате (pdf и txt), которые будут добавлены в базу знаний и по которым в том числе будет генерироваться отчёт. Сканы в pdf файлах не будут обрабатываться, только текстовые данные.
5. **Search in the internet** (опциональное) - если этот флаг не установлен, то отчёт будет генерироваться только на основе пользовательских ссылок (из п.1 **New source**) и пользовательских документов (из п.4 **Your data files**). Если установлен, то информация будет браться из открытых источников в интернете.

Для запуска генерации отчёта необходимо заполнить обязательные поля и нажать на конпку **Analyse**.
Отчёт будет сгенерирован в орфмате docx. После генерации появится кнопка скачать.

<img width="173" alt="image" src="https://github.com/MisterAndry/lct2024-rag/assets/9989672/e8f0f179-3057-456c-9c4b-8b715eebe424">


## Локальный запуск
1. Установить ключ для OpenAI на 17 строчке в файлe **rag.py** по пути **backend/models/rag.py**
2. Перейти в корневой каталог репозитория
3. Прописать в консоли **docker-compose up**
4. Приложение заработает по адресу **http://localhost:8080**