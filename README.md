My Cloud – Облачное файловое хранилище
Дипломный проект по профессии «Fullstack-разработчик на Python».
My Cloud — веб-приложение, позволяющее пользователям загружать, скачивать, удалять и делиться файлами через специальные ссылки. Реализовано на Django + React с развёртыванием на reg.ru.

Ссылка на рабочий проект: http://83.166.245.243
Ссылка на репозиторий: https://github.com/e1ectron1k/diplomeFN

Стек технологий
Бэкенд: Python 3.12, Django 4.2, Django REST framework, PostgreSQL, Gunicorn

Фронтенд: React 19, Redux Toolkit, React Router 7, Axios, CSS (адаптивная вёрстка)

Инфраструктура: Nginx, PostgreSQL, Gunicorn, systemd, Git, Reg.ru (Ubuntu 24.04)

Дополнительно: Drag & Drop загрузка, прогресс-бар загрузки, адаптивный дизайн

Репозиторий
Проект хранится на GitHub:
https://github.com/e1ectron1k/diplomeFN

Структура репозитория
text
diplome/
├── backend/                  # Django проект
│   ├── apps/                 # Приложения users и files
│   ├── config/               # Настройки Django
│   ├── manage.py
│   └── requirements.txt
├── frontend-cra/             # React приложение (создано через CRA)
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
Требования для локального запуска
Python 3.10+

Node.js 18+ и npm

PostgreSQL 14+

Инструкция по развёртыванию на сервере reg.ru
Детальная инструкция есть в репозитории, основные шаги:

Установить PostgreSQL, Nginx, Python, Node.js.

Склонировать проект.

Настроить бэкенд (виртуальное окружение, .env, миграции).

Собрать фронтенд (npm run build) и скопировать в /var/www/mycloud.

Настроить Gunicorn (systemd) и Nginx.

При необходимости включить HTTPS через Certbot.

API (краткое описание)
Все эндпоинты имеют префикс /api/.

Метод	URL	Описание	Доступ
POST	/users/register/	Регистрация	Публичный
POST	/users/login/	Вход	Публичный
POST	/users/logout/	Выход	Авторизованный
GET	/users/me/	Текущий пользователь	Авторизованный
GET	/users/	Список пользователей	Администратор
DELETE	/users/<id>/	Удаление пользователя	Администратор
GET	/files/	Список файлов	Авторизованный
POST	/files/	Загрузка файла	Авторизованный
GET	/files/<id>/download/	Скачивание файла	Авторизованный
DELETE	/files/<id>/	Удаление файла	Авторизованный
POST	/files/<id>/generate-link/	Генерация специальной ссылки	Авторизованный
GET	/files/special/<uuid>/	Скачивание по специальной ссылке	Публичный
Тестовые учётные данные
Администратор: создаётся через createsuperuser (флаг is_admin нужно установить вручную в БД или через админку).

Обычный пользователь: можно зарегистрировать через интерфейс.

Автор
Студент: Чалов Сергей
GitHub: https://github.com/e1ectron1k
Дата: Март 2026
