[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Wildberries+Bot)](https://git.io/typing-svg)

Это телеграм-бот, созданный для установки напоминаний. Бот помогает пользователям создавать задачи, устанавливать для них напоминания на основе временных интервалов (минуты, часы, дни, недели, месяцы) и просматривать активные задачи.

# Функционал:
_Создание напоминаний — Пользователь может создать задачу с указанием временного интервала._

_Просмотр активных задач — Пользователь может просмотреть список всех активных напоминаний с помощью команды /view._


# Технологии, использованные в боте:
Python — Основной язык программирования для создания бота.

Aiogram — Асинхронная библиотека для разработки Telegram ботов на Python.

PostgreSQL — База данных для хранения информации о пользователях и напоминаниях.

SQLAlchemy — ORM (Object-Relational Mapping) для взаимодействия с базой данных.

APScheduler — Планировщик задач для управления напоминаниями, их созданием и отправкой в нужное время.

Docker — Для контейнеризации приложения, что облегчает его развертывание и запуск на любых серверах.

dotenv — Для работы с переменными окружения через файл .env.


# Требования:

Python 3.10+: Убедитесь, что Python установлен. Скачать можно с python.org.

Аккаунт Telegram: Необходим для взаимодействия с ботом.

Токен бота: Получите токен бота, создав нового бота через BotFather в Telegram.


# Установка и запуск бота:

_1. Клонирование репозитория_
Сначала клонируйте репозиторий с исходным кодом бота:

Копировать код: 

    •	git clone <URL вашего репозитория>
    •	cd <название-проекта>

_2. Настройка проекта_

Создайте и активируйте виртуальную среду (опционально, но рекомендуется):

    •	python -m venv venv
    •	Для Windows: venv\Scripts\activate

Установите зависимости:

    •	pip install -r requirements.txt

_3. Настройка файла .env_

Создайте файл .env на основе шаблона .env.example. Пример содержимого файла .env:

    •	TOKEN=<ваш-токен-для-бота>
    •	DATABASE_URL=postgresql://<имя-пользователя>:<пароль>@<хост>:<порт>/<имя-базы>

TOKEN — токен вашего Telegram бота, полученный через BotFather.

DATABASE_URL — строка подключения к базе данных PostgreSQL.

_4. Инициализация базы данных_

Для инициализации базы данных выполните следующую команду:

    •	python -c "from bot.models import Base, engine; Base.metadata.create_all(engine)"

Эта команда создаст необходимые таблицы в базе данных.

_5. Запуск бота_

Чтобы запустить бота, используйте следующую команду:

    •	python bot.py

# Использование Docker

Для упрощения развертывания приложения можно использовать Docker. В проекте уже есть Dockerfile, что позволяет контейнеризировать приложение.

_1. Сборка Docker-образа_

Убедитесь, что файл Dockerfile настроен правильно. Далее выполните команду для сборки Docker-образа:

    •	docker build -t wildberries-reminder-bot .

_2. Запуск Docker-контейнера_
   
После сборки Docker-образа, создайте контейнер и запустите его, передав переменные окружения через файл .env:

    •	docker run --env-file .env -d wildberries-reminder-bot

_3. Остановка контейнера_

Чтобы остановить запущенный контейнер, выполните следующую команду:

    •	docker stop <ID контейнера>

# Заключение

После выполнения всех шагов бот будет успешно запущен и готов к использованию. Если возникнут вопросы или потребуется дополнительная настройка, вы всегда можете следовать этой документации.
