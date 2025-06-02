"""
Настройки для тестового окружения.
Оптимизированы для быстрого выполнения тестов.
"""

from .base import *

# Отключаем отладку в тестах
DEBUG = False

ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Отключаем debug toolbar для тестов
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE if 'debug_toolbar' not in middleware]

# Используем SQLite в памяти для быстрых тестов
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        },
        'OPTIONS': {
            'timeout': 20,
        },
    }
}

# Отключаем миграции для ускорения тестов


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Простое кэширование в памяти
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
        'TIMEOUT': 300,
    }
}

# Отключаем password validation для тестов
AUTH_PASSWORD_VALIDATORS = []

# Email backend для тестов
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Статические файлы для тестов
STATIC_ROOT = '/tmp/static_test'

# Медиа файлы для тестов
MEDIA_ROOT = '/tmp/media_test'

# Локализация для тестов - используем английский
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

# Логирование для тестов - минимальное
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Настройки для тестирования API
REST_FRAMEWORK_TEST = REST_FRAMEWORK.copy()
REST_FRAMEWORK_TEST.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_VERSIONING_CLASS': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': None,
})

# Переопределяем REST_FRAMEWORK для тестов
REST_FRAMEWORK = REST_FRAMEWORK_TEST

# Быстрый хешер паролей для тестов
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Отключаем timezone для тестов
USE_TZ = False

# Настройки для тестирования файлов
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB для тестов
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB для тестов

# Настройки для spectacular в тестах
SPECTACULAR_SETTINGS.update({
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'SERVERS': [
        {
            'url': 'http://testserver',
            'description': 'Test server'
        },
    ],
})
