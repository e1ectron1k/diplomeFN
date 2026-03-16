# My Cloud – Облачное файловое хранилище

Дипломный проект по профессии «Fullstack-разработчик на Python».  
My Cloud — веб-приложение, позволяющее пользователям загружать, скачивать, удалять и делиться файлами через специальные ссылки. Реализовано на Django + React с развёртыванием на reg.ru.

---

## Стек технологий

- **Бэкенд:** Python 3.13, Django 4.2, Django REST framework, PostgreSQL, Gunicorn
- **Фронтенд:** React 19, Redux Toolkit, React Router 7, Axios, CSS (адаптивная вёрстка)
- **Инфраструктура:** Nginx, PostgreSQL, Gunicorn, systemd, Git, Reg.ru (Ubuntu 24.04)
- **Дополнительно:** Drag & Drop загрузка, прогресс-бар загрузки, адаптивный дизайн

---

## Репозиторий

Проект хранится на GitHub в виде монорепозитория:
https://github.com/e1ectron1k/diplome.git
---

## Структура репозитория
my-cloud/
├── backend/ # Django проект
│ ├── apps/ # Приложения users и files
│ ├── config/ # Настройки Django
│ ├── manage.py
│ └── requirements.txt
│ 
├── frontend-cra/ # React приложение
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── ... # остальные файлы конфигурации
└── README.md # Этот файл

---

1. Клонирование проекта с GitHub
bash
cd /root
git clone https://github.com/your-username/my-cloud.git
cd my-cloud
2. Настройка базы данных
bash
sudo -u postgres psql
CREATE USER dbuser WITH PASSWORD 'your_strong_password';
CREATE DATABASE mycloud OWNER dbuser;
\q
3. Бэкенд
bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn psycopg2-binary
Создайте файл .env с содержимым (пример ниже):

ini
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your_server_ip,your_domain.com
DB_NAME=mycloud
DB_USER=dbuser
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432
STATIC_ROOT=/root/my-cloud/backend/static
MEDIA_ROOT=/root/my-cloud/backend/media
Примените миграции и соберите статику:

bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser   # создайте администратора
4. Фронтенд (сборка статики)
bash
cd ../frontend-cra
npm install
npm run build
Скопируйте собранные файлы в папку для Nginx:

bash
mkdir -p /var/www/mycloud
cp -r build/* /var/www/mycloud/
5. Настройка Gunicorn (systemd)
Создайте файл /etc/systemd/system/gunicorn_mycloud.service:

text
[Unit]
Description=gunicorn daemon for mycloud
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/my-cloud/backend
Environment="PATH=/root/my-cloud/backend/venv/bin"
ExecStart=/root/my-cloud/backend/venv/bin/gunicorn --workers 3 --bind unix:/root/my-cloud/backend/mycloud.sock config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
Запустите и добавьте в автозагрузку:

bash
systemctl start gunicorn_mycloud
systemctl enable gunicorn_mycloud
6. Настройка Nginx
Создайте файл /etc/nginx/sites-available/mycloud:

nginx
server {
    listen 80;
    server_name your_server_ip your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        root /var/www/mycloud;
        try_files $uri /index.html;
    }

    location /static/ {
        alias /root/my-cloud/backend/static/;
    }

    location /media/ {
        alias /root/my-cloud/backend/media/;
    }

    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/root/my-cloud/backend/mycloud.sock;
    }

    location /admin/ {
        include proxy_params;
        proxy_pass http://unix:/root/my-cloud/backend/mycloud.sock;
    }
}
Активируйте сайт:

bash
ln -s /etc/nginx/sites-available/mycloud /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
7. Настройка HTTPS (опционально, но рекомендуется)
bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your_domain.com
8. Проверка
Откройте браузер и перейдите по IP или домену. Протестируйте все функции.

Автоматизация обновлений (скрипт деплоя)
На сервере можно создать скрипт для быстрого обновления после пуша в Git:

bash
#!/bin/bash
cd /root/my-cloud
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd ../frontend-cra
npm install
npm run build
cp -r build/* /var/www/mycloud/
systemctl restart gunicorn_mycloud
systemctl reload nginx
Сохраните как /root/deploy.sh, сделайте исполняемым (chmod +x deploy.sh).

API (краткое описание)
Все эндпоинты имеют префикс /api/.

Метод	URL	Описание	Доступ
POST	/users/register/	Регистрация	Публичный
POST	/users/login/	Вход	Публичный
POST	/users/logout/	Выход	Авторизованный
GET	/users/me/	Текущий пользователь	Авторизованный
GET	/users/	Список пользователей	Администратор
PATCH	/users/<id>/	Обновление пользователя	Администратор
DELETE	/users/<id>/	Удаление пользователя	Администратор
GET	/files/	Список файлов	Авторизованный
POST	/files/	Загрузка файла	Авторизованный
GET	/files/<id>/download/	Скачивание файла	Авторизованный
DELETE	/files/<id>/	Удаление файла	Авторизованный
POST	/files/<id>/generate-link/	Генерация специальной ссылки	Авторизованный
GET	/files/special/<uuid>/	Скачивание по специальной ссылке	Публичный
Тестовые учётные данные
Администратор:
Логин: admin
Пароль: (создаётся через createsuperuser)

Обычный пользователь: можно зарегистрировать через интерфейс.

Возможные улучшения
Добавление папок (многоуровневое хранилище)

Шаринг файлов между пользователями

Предпросмотр изображений и видео

Отправка уведомлений на почту

Автор
Студент: [Ваше имя]
Курс: Fullstack-разработчик на Python
GitHub: https://github.com/your-username
Дата: Март 2026

Ссылка на рабочий проект: http://your-server-ip/
Ссылка на репозиторий: https://github.com/your-username/my-cloud