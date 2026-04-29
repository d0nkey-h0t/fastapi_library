# 📚 Library Manager API

Учебное веб-приложение на **FastAPI**, реализующее RESTful API для управления библиотекой: добавление, просмотр, редактирование и удаление книг.

Использует асинхронную работу с базой данных через **SQLAlchemy (async)** и **SQLite** в качестве хранилища.

---

## 🛠️ Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — современный фреймворк для создания API на Python.
- [SQLAlchemy 2.0+](https://docs.sqlalchemy.org/) — ORM для работы с базой данных (асинхронный режим).
- [Pydantic v2](https://docs.pydantic.dev/latest/) — валидация данных и схемы.
- [SQLite](https://www.sqlite.org/) — лёгкая встраиваемая СУБД (файл `library.db`).
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер для запуска приложения.
- [Poetry](https://python-poetry.org/) — менеджер зависимостей и пакетов (опционально)

---

## 📁 Структура проекта

```
.
├── main.py               # Точка входа, настройка приложения и lifespan
├── config.py             # Константы (имя БД, сообщения об ошибках)
├── database.py           # Настройка БД: движок, сессия, базовый класс моделей
├── models/
│   └── books.py          # Модель книги (SQLAlchemy)
├── schemas/
│   └── books.py          # Схемы Pydantic для валидации
├── repositories/
│   └── books.py          # Логика работы с книгами (CRUD)
├── routers/
│   └── books.py          # Роутер FastAPI для `/books`
├── pyproject.toml        # Зависимости и метаданные (для Poetry)
└── README.md             # Этот файл
```

---

## 🚀 Запуск проекта

### Предварительные требования

- Python 3.10+
- Установленный [Poetry](https://python-poetry.org/docs/#installation) (опционально)

---

### Установка и запуск

Вы можете запустить проект двумя способами: через `pip` или через `poetry`.

#### 🔹 Способ 1: Через Poetry (рекомендуется)

> Poetry — современный менеджер зависимостей для Python. Он автоматически создаёт виртуальное окружение и управляет зависимостями.

1. Установите зависимости:
   ```bash
   poetry install
   ```

2. Активируйте виртуальное окружение:
   ```bash
   poetry shell
   ```

3. Запустите сервер:
   ```bash
   python main.py
   ```
   Или, если вы используете скрипт:
   ```bash
   poetry run start
   ```

> 💡 При первом запуске будет создан файл `library.db` и таблица `books`.

---

#### 🔹 Способ 2: Через pip и виртуальное окружение

```bash
# 1. Клонируйте репозиторий (если нужно)
git clone https://github.com/ваш-пользователь/library-api.git
cd library-api

# 2. Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate    # Linux/macOS
# или
venv\Scripts\activate       # Windows

# 3. Установите зависимости
# Сначала создайте requirements.txt из pyproject.toml или используйте:
poetry export --with=main --format=requirements.txt --output=requirements.txt
pip install -r requirements.txt

# 4. Запустите сервер
python main.py
```

> ⚠️ Если у вас нет `requirements.txt`, лучше использовать Poetry напрямую.

---

## 🌐 Доступные эндпоинты

После запуска API будет доступно по адресу: `http://127.0.0.1:8080`

Документация Swagger (автоматически генерируется):  
👉 [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

| Метод | Путь            | Описание                     |
|-------|------------------|------------------------------|
| POST  | `/books`         | Добавить новую книгу         |
| GET   | `/books`         | Получить все книги           |
| GET   | `/books/{id}`    | Получить книгу по ID         |
| PUT   | `/books/{id}`    | Обновить книгу                |
| DELETE| `/books/{id}`    | Удалить книгу                 |

---

## 📘 Примеры запросов

### Добавить книгу

```json
POST /books
{
  "title": "1984",
  "author": "George Orwell",
  "year": 1949,
  "pages": 328,
  "is_read": true
}
```

✅ Ответ: `201 Created`, возвращает созданную книгу с `id`.

---

### Получить все книги

```json
GET /books
```

✅ Ответ: `200 OK`, массив всех книг.

---

### Получить книгу по ID

```json
GET /books/1
```

✅ Ответ: `200 OK`, объект книги.

❌ Если не найдена: `404 Not Found` → `"Book not found"`

---

### Обновить книгу

```json
PUT /books/1
{
  "title": "1984 (Updated)",
  "author": "George Orwell",
  "year": 1950,
  "pages": 330,
  "is_read": false
}
```

✅ Ответ: `200 OK`, обновлённая книга.

---

### Удалить книгу

```http
DELETE /books/1
```

✅ Ответ: `204 No Content`

---

## 🔐 Валидация

- Поле `pages` должно быть ≥ 10.
- Поле `is_read` по умолчанию `false`.
- Все поля обязательны, кроме `is_read`.

---

## ⚙️ Конфигурация

Файл: `config.py`

```python
DB_NAME = "library"           # Имя файла БД: library.db
MSG_NOT_FOUND = "Book not found"
```

> Чтобы изменить имя БД — просто поменяйте `DB_NAME`.

---

## 🧪 Особенности реализации

- **Асинхронность**: все операции с БД выполняются асинхронно.
- **Разделение ответственности**:
  - `models` — структура таблицы.
  - `schemas` — валидация входных/выходных данных.
  - `repositories` — логика работы с БД.
  - `routers` — HTTP-роуты.
- **Lifespan**: при старте создаётся таблица `books`, если её нет.

---

## 📦 Управление зависимостями

Проект поддерживает **Poetry**. Файл `pyproject.toml` содержит все зависимости:

```toml
[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.32.0"}
sqlalchemy = {extras = ["asyncio"], version = "^2.0.36"}
pydantic = {extras = ["dotenv"], version = "^2.8.2"}

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
httpx = "^0.27.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
start = "main:main"
```

> Чтобы добавить новую зависимость: `poetry add имя_пакета`  
> Чтобы добавить dev-зависимость: `poetry add --group dev pytest`

---

## 📄 Лицензия

Этот проект распространяется без лицензии. Вы можете использовать его для обучения и модификации.

---

## 🙌 Автор

> Этот проект был разработан как обучающий пример для курса по FastAPI.

Хорошего кода и счастливого чтения! 📖