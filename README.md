<p align="center"><img width=12.5% src="https://github.com/anfederico/clairvoyant/blob/master/media/Logo.png"></p>
<p align="center"><img width=60% src="https://github.com/anfederico/clairvoyant/blob/master/media/Clairvoyant.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/clairvoyant.svg)](https://github.com/anfederico/clairvoyant/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

1. 🌀 [Описание проекта](#what-is-this)
2. 🌟 [Возможности сервиса](#features)
2. 📈 [Описание схемы БД](#database_scheme)
3. 🚀 [Инструкция по установке](#installation)
5. 💯 [Тесты](#tests)
6. ©️ [License](#license)

## <a name="what-is-this-api"> 🌀 Описание проекта</a>

Share & Park представляет собой веб-сервис краткосрочной аренды парковочных мест. Благодаря своим функциям сервис выступает в качестве площадки, на которой владельцы парковочных мест могут предложить услуги аренды всем заинтересованным автовладельцам.
HardQode_solution - backend-сервис на основе Django REST Framework, представляющий собой учебный портал с курсами различных категорий. В каждый курс входит каталоге уроков. Некоторые уроки состоят в нескольких курсах. Сервис предоставляет пользователю доступ к списку доступных ему уроков, на приобретеных курсах. Также пользователь получает доступ к детальной статистике по всем курсам. База данных - SQLite. Зависимости - Poetry. Линтеры - Black, Flake8. Контейнеризация - Docker

## <a name="features"> 🌟 Возможности сервиса </a>

<details>
<summary>Возможность</summary>
<br>
Описание фичи
</details>

<details>
<summary>Возможность</summary>
<br>
Описание фичи
</details>

<details>
<summary>Возможность</summary>
<br>
Описание фичи
</details>

## <a name="database_scheme"> 📈 База данных </a>
База данных содержит 6 моделей: Author(Автор публикации), Category(Категория публикации), Post(Публикация), PostCategory(Публикация в категории) Comment(Комментарий), UserCategory(Подписчики на категорию). Ниже представлена графическая схема моделей и их взаимосвязей.

![Screen Shot](extras/erd.png)


## <a name="database_scheme"> 🚀 Инструкция по установке

1. ### Подготовка проекта

1.1 Клонируете репозиторий
```sh
git clone https://github.com/XanderMoroz/GoodNews-DRF.git
```

1.2 В корневой папки клонированного репозитория создаете файл .env

1.3 Заполните файлe .env по следующему шаблону:

```sh
# DJANGO DEFAULT SETTINGS
SECRET_KEY='django-insecure-#)!-t1b(7&wr_7c%0m%w$(y@^#z6wizw^trm$dtz70@m1fe$6*'

# POSTGRESQL DEFAULT DATABASE
POSTGRES_USER=postgres
POSTGRES_PASS=postgres
POSTGRES_HOST=postgres  #localhost(при использовании локально)  
POSTGRES_PORT=5432
POSTGRES_DB=goodnews

```
2. ### Запуск проекта с Doker
2.1 Создаете и запускаете контейнер через терминал:
```sh
sudo docker-compose up -d
```
2.2 Создайте суперпользователя и заполните поля:
```sh
sudo docker exec -it goodnews-drf_web_1 python manage.py createsuperuser
```
2.3 Сервис доступен по адресу: http://0.0.0.0:8000/

## <a name="tests"> 💯 Тесты



## <a name="license"> ©️ License
