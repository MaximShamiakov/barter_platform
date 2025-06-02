# Barter Platform

Платформа для обмена товарами - веб-приложение, позволяющее пользователям размещать объявления о товарах и предлагать обмен.

## Описание проекта

Barter Platform - это веб-платформа для обмена товарами между пользователями. Система позволяет создавать объявления о товарах, искать интересные предложения и организовывать обмен без использования денег.

## Функциональность

### Основные возможности:
- **Регистрация и авторизация** пользователей
- **Создание объявлений** о товарах для обмена
- **Поиск и фильтрация** объявлений по категориям и состоянию
- **Система предложений обмена** между пользователями
- **Управление статусами** предложений (принять/отклонить)
- **REST API**
- **Многоязычность** (русский/английский)
- **Административная панель** для модерации

## Технологии

- **Backend**: Python 3.11, Django 4.2
- **API**: Django REST Framework
- **База данных**: PostgreSQL
- **API Документация**: drf-spectacular (Swagger)
- **Тестирование**: Django TestCase
- **Локализация**: Django i18n
- **Кэширование**: LocMem (development)
- **Логирование**: Python logging

## Установка и настройка

### Вариант 1: Использование Docker (VSCode Dev Container)

1. **Клонирование репозитория:**
```bash
git clone <repository-url>
cd barter_platform
```

2. **Настройка переменных окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл при необходимости
```

3. **Запуск через Dev Container (VS Code):**
```bash
# Откройте проект в VS Code
# Нажмите Ctrl+Shift+P и выберите "Dev Containers: Reopen in Container"
```

### Вариант 2: Локальная установка

1. **Создание виртуального окружения:**
```bash
python -m venv .venv
source .venv/bin/activate
```

2. **Установка зависимостей:**
```bash
pip install -r requirements/development.txt
```

3. **Настройка базы данных:**
```bash
# Создайте базу данных PostgreSQL
createdb barter_platform

# Настройте переменные в .env
echo "DB_NAME=barter_platform" >> .env
echo "DB_USER=your_user" >> .env
echo "DB_PASSWORD=your_password" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
```

4. **Выполнение миграций:**
```bash
python manage.py migrate
```

5. **Создание суперпользователя:**
```bash
python manage.py createsuperuser
```

## Запуск проекта

### Development окружение:

```bash
# Запуск сервера разработки
DJANGO_ENV=development python manage.py runserver
```

Приложение будет доступно по адресу: http://localhost:8000

### Административная панель:
http://localhost:8000/admin/

### API Документация:
- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI схема: http://localhost:8000/api/schema/

## Тестирование

### Запуск всех тестов:
```bash
DJANGO_ENV=testing python manage.py test
```

### Запуск тестов с покрытием:
```bash
DJANGO_ENV=testing coverage run --source='.' python manage.py test
coverage report
coverage html
# Отчет будет в htmlcov/
```


## Локализация

### Поддерживаемые языки:
- Русский (ru) - по умолчанию
- Английский (en)

### Создание/обновление переводов:

1. **Извлечение строк для перевода:**
```bash
python manage.py makemessages -l en
python manage.py makemessages -l ru
```

2. **Компиляция переводов:**
```bash
python manage.py compilemessages
```

### Файлы переводов:
- `locale/en/LC_MESSAGES/django.po` - Английские переводы
- `locale/ru/LC_MESSAGES/django.po` - Русские переводы

### Переключение языка:
- В веб-интерфейсе: используйте переключатель языка
- В API нужно передавать заголовок `Accept-Language: en` или `Accept-Language: ru`

## Структура проекта

```
barter_platform/
  .devcontainer/          # Настройки Docker контейнера для разработки
  .vscode/                # Настройки VS Code
  api/                    # REST API приложения
  apps/                   # Django приложения
  config/                 # Настройки Django
    settings/
      base.py               # Базовые настройки
      development.py        # Настройки разработки
      testing.py            # Настройки для тестов
    urls.py                 # Главные URL маршруты
    wsgi.py
    asgi.py
  locale/                 # Файлы локализации
  requirements/           # Зависимости Python
    base.txt              # Базовые зависимости
    development.txt       # Зависимости для разработки
    testing.txt           # Зависимости для тестирования
  static/                 # Статические файлы
  templates/              # HTML шаблоны
  .env.example            # Пример переменных окружения
  .gitignore
  manage.py
  README.md
```

## Логирование

### Настройка логов:

Логи настраиваются в `config/settings/base.py` и переопределяются в специфичных настройках окружения.

### Уровни логирования:
- **DEBUG**: Детальная информация для отладки
- **INFO**: Общая информация о работе приложения
- **WARNING**: Предупреждения о потенциальных проблемах
- **ERROR**: Ошибки, которые не приводят к остановке
- **CRITICAL**: Критические ошибки

### Просмотр логов:
```bash
# Development
tail -f /tmp/barter_platform_logs/django.log
```
