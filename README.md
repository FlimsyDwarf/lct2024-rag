# Автоматическая генерация аналитических отчётов (ЛЦТ 2024)


![image](https://github.com/FlimsyDwarf/lct2024-rag/assets/72410090/b6a204de-78b4-4629-a7bb-a2bc291da807)



## Принцип работы

### Описание полей ввода UI
1. **New source** (опциональное) - поле ввода ссылок на статьи или любое другие ресурсы, которые будут парситься, добавляться в базу знаний. Вводятся по одной.
2. **Date Range** (опциональное) - временные рамки, по которым будет строиться отчёт. Можно указать как только левую границу дат, так и обе - левую и правую. Например, нужен анализ какого-то рынка только за 2020-2023 год.
3. **Template File** (обязательное) - файл шаблона в формате docx, содержащий запросы, по которым будет прозведен анализ и составлен отчёт.
   
   Шаблон обязательно должен включать в себя:
   1) Заголовок - только *первая* строка файла шаблона
   2) Главную тему анализа, то есть его направленность - только *вторая* строка файла шаблона
   3) Блоки с запросами в следующем формате:
      - Каждый блок должен начинаться со слова «Блок»
      - Слово «Блок» в любом регистре не должно встречаться в тексте шаблона где-либо, кроме названий блоков
      - Название блока располагается в отдельной строке, может отсутствовать
      - Внутри блока расположены только *пронумерованные* или *промаркированные* строки - точные запросы. Одна строка - один запрос.
      - Внутри каждого блока должен быть хотя бы *один* запрос

   Пример:

![image](https://github.com/FlimsyDwarf/lct2024-rag/assets/72410090/b2a7644a-19d1-4221-95ae-27fd84d3c615)



4. **Your data files** (опциональное) - пользовательские файлы в формате (pdf и txt), которые будут добавлены в базу знаний и по которым в том числе будет генерироваться отчёт. Сканы в pdf файлах не будут обрабатываться, только текстовые данные.
5. **Search in the internet** (опциональное) - если эта галочка не установлена, то отчёт будет генерироваться только на основе пользовательских ссылок (из п.1 **New source**) и пользовательских документов (из п.6 **Your data files**). Если установлен, то информация будет браться из открытых источников в интернете.
7. **Аmount of links** (опциональное) - количество результатов поиска, полученных по каждому подпункту при поиске информации в Интернете (стандартное значение: 5) 

Для запуска генерации отчёта необходимо заполнить обязательные поля и нажать на конпку **Analyse**.
Отчёт будет сгенерирован в орфмате docx. После генерации появится кнопка скачать.

![image](https://github.com/FlimsyDwarf/lct2024-rag/assets/72410090/c6ae7e38-e821-49f4-9f87-65ae31141065)




## Templates

По нажатию кнопки **Templates** в правом верхнем углу появится меню с двумя файлами:
   1) Шаблон анализа конкурентов
   2) Анализ компании "Газпром"

![image](https://github.com/FlimsyDwarf/lct2024-rag/assets/72410090/6338d181-4b16-4fd8-94d0-d16af08e68b3)


Это примеры файла шаблона для анализа и файла отчета.
Их можно скачать по нажатию.


## Локальный запуск
1. Установить ключ для OpenAI на 17 строчке в файлe **rag.py** по пути **backend/models/rag.py**
2. Перейти в корневой каталог репозитория
3. Прописать в консоли **docker-compose up**
4. Приложение заработает по адресу **http://localhost:8080**
