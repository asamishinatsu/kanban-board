# Kanban Board

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&logoColor=black)

Веб-приложение для управления досками задач и личной продуктивностью (аналог Trello). Позволяет пользователям организовывать работу через гибкую трехуровневую структуру: доски, списки и карточки.

<!-- Добавь сюда скриншот интерфейса: положи картинку в папку assets/ или docs/ -->
<!-- ![Скриншот интерфейса](docs/preview.png) -->

---

## Основные возможности

* **Аутентификация и безопасность:**
  * Регистрация и авторизация пользователей с сохранением сессий (`Flask-Login`).
  * Строгая изоляция данных: пользователь имеет доступ только к собственным доскам.
* **Управление задачами (CRUD):**
  * Полный цикл создания, редактирования и удаления досок, списков и карточек.
  * Настройка приоритетов карточек (`low`, `medium`, `high`) и установка сроков выполнения (дедлайнов).
* **Интерактивный интерфейс:**
  * Серверный рендеринг страниц через Jinja2.
  * Модальные окна подтверждения для деструктивных действий (удаление).
  * Динамическое управление элементами через Vanilla JavaScript и DOM API.

---

## Стек технологий

* **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login.
* **Database:** SQLite (локально в разработке).
* **Frontend:** Jinja2 templates, HTML5, CSS3, JavaScript (ES6).

---

## Архитектура проекта

```text
src/
├── main.py          # Инициализация приложения, конфигурация и маршрутизация (routes)
├── models.py        # Модели данных: User, Board, CardList, Card
├── extensions.py    # Экземпляр базы данных SQLAlchemy
├── secret.py        # Конфигурация секретного ключа (исключен из Git)
├── static/          # Стили CSS, клиентский JavaScript, шрифты
└── templates/       # HTML-шаблоны страниц
```

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/asamishinatsu/kanban-board.git
cd kanban-board
```

### 2. Настройка виртуального окружения

**На Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**На Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
*(Либо вручную: `pip install Flask Flask-Login Flask-SQLAlchemy`)*

### 4. Конфигурация секретного ключа
Создайте файл `src/secret.py`:
```python
SECRET_KEY = 'replace-with-a-random-secret-key'
```

### 5. Запуск приложения
```bash
python src/main.py
```
При первом запуске база данных SQLite создается автоматически в директории `instance/`.  
Сервис будет доступен по адресу: **http://127.0.0.1:8080**

---

## Схема маршрутов (Endpoints)

| Метод | URL | Описание |
| :--- | :--- | :--- |
| `GET` | `/` / `/board_list` | Главная страница со списком досок пользователя |
| `POST` | `/register` / `/login` | Регистрация и авторизация |
| `GET` | `/logout` | Завершение сессии пользователя |
| `GET` | `/board/<board_id>` | Просмотр конкретной доски со списками и карточками |
| `POST` | `/board/create` | Создание новой доски |
| `POST` | `/board/<id>/edit`, `delete` | Редактирование и удаление доски |
| `POST` | `/board/<id>/list/create` | Добавление списка на доску |
| `POST` | `/list/<id>/edit`, `delete` | Редактирование и удаление списка задач |
| `POST` | `/list/<id>/card/create` | Создание карточки задачи |
| `POST` | `/card/<id>/edit`, `delete` | Редактирование (смена приоритета, дедлайна) и удаление карточки |
