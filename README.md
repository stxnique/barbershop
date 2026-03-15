# BarberX — Веб-приложение для барбершопа

Веб-приложение для автоматизации записи в барбершоп. Разработано на Django с PostgreSQL.

## Функционал
- Онлайн-запись на стрижку
- Каталог услуг и барберов
- Регистрация и вход по телефону/email
- Админ-панель для управления

## Технологии
- Python, Django
- HTML5, CSS3, JavaScript
- PostgreSQL
- Git, GitHub

## Установка и запуск

```bash
# 1. Клонируй репозиторий
git clone https://github.com/stxnique/barberx.git
cd barberx

# 2. Создай и активируй виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 3. Установи зависимости
pip install django psycopg2-binary

# 4. Настрой PostgreSQL в webapp/settings.py
#    Имя БД: barberx_db, пользователь: postgres, пароль: твой

# 5. Создай БД в PostgreSQL
#    CREATE DATABASE barberx_db;

# 6. Примени миграции
python manage.py makemigrations
python manage.py migrate

# 7. Создай суперпользователя
python manage.py createsuperuser

# 8. Запусти сервер
python manage.py runserver
