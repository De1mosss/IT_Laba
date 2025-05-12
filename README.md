# YandexForm

API-приложение для создания, управления формами и сбора ответов.

## Основные технологии

* Python 3.11+
* Flask 3.x
* Flask-SQLAlchemy
* Flask-Migrate (Alembic)
* Flask-JWT-Extended
* Swagger UI (статический `swagger.json`)

## Файловая структура

```
summer_laba/
├── .venv/                   # виртуальное окружение
├── instance/               # здесь будет храниться SQLite база (app.db)
├── migrations/             # папка миграций Alembic
├── yandexform/             # основное приложение (пакет)
│   ├── __init__.py         # фабрика create_app(), регистрация Blueprints и миграций
│   ├── config.py           # класс Config (переменные окружения)
│   ├── models/             # модели SQLAlchemy
│   ├── routes/             # маршруты (auth, form, response)
│   ├── services/           # логика (регистрация, формы, ответы)
│   ├── utils/              # вспомогательные утилиты, auth_utils и т.п.
│   └── static/             # статические файлы, включая swagger.json
├── app.py                  # точка входа: `from yandexform import create_app`
├── requirements.txt        # зависимости
└── README.md               # этот файл
```

## Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
# Клонируем репозиторий
git clone <URL>
cd summer_laba

# Создаем и активируем виртуальное окружение
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.flaskenv` или экспортируйте переменные вручную.

Вариант 1: `.flaskenv` в корне проекта:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
# необязательно, если хотите использовать SQLite:
DATABASE_URL=sqlite:///instance/app.db
```

Вариант 2: вручную в терминале:

```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
$env:SECRET_KEY = 'your-secret-key'
$env:DATABASE_URL = 'sqlite:///instance/app.db'
```

### 3. Инициализация базы данных и миграции

```bash
# Создайте папку instance, если её нет (фабрика create_app() делает это автоматически)
# Запускаем миграции
flask db init      # только первый раз
flask db migrate -m "Initial migration"
flask db upgrade
```

> **Примечание:** при старте `create_app()` функция автоматически вызывает `upgrade()` и `db.create_all()`

### 4. Запуск приложения

```bash
python app.py
```

По умолчанию сервер доступен на `http://127.0.0.1:5000`.

### 5. Документация Swagger

После запуска откройте в браузере:

```
http://127.0.0.1:5000/api/docs/
```

Swagger UI загрузит `static/swagger.json` и отобразит все эндпоинты.

## Краткое описание эндпоинтов

### Auth

* `POST /auth/register` — регистрация

  * Body: `{ "username": "string", "password": "string" }`
  * Ответ 201, 400
* `POST /auth/login` — вход

  * Body: `{ "username": "string", "password": "string" }`
  * Ответ 200 `{ token, user_id }`, 400, 401

### Forms (JWT required)

* `POST /form/forms`
* `GET  /form/forms`
* `GET  /form/forms/{form_id}`
* `PUT  /form/forms/{form_id}`
* `DELETE /form/forms/{form_id}`

### Responses (JWT required)

* `POST /api/responses/{form_id}`
* `GET  /api/responses/{form_id}`

Для защищённых маршрутов добавляйте заголовок:

```
Authorization: Bearer <JWT>
```

---

## Полезные команды

* `flask db migrate -m "msg"` — создать миграцию
* `flask db upgrade` — применить миграции
* `flask run` — запустить сервер (если FLASK\_APP задан)

---

## Контакты

По вопросам — создайте issue в этом репозитории или напишите автору.
