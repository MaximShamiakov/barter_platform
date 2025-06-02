# Тесты локализации (unit тесты)
# Этот файл был перенесен из apps/ads/test_localization.py

from django.test import TestCase
from django.utils.translation import activate, gettext


class LocalizationTest(TestCase):
    """Тесты для проверки локализации."""

    def test_russian_localization(self):
        """Тест русской локализации."""
        activate('ru')

        # Проверяем основные переводы
        self.assertEqual(gettext('Категория'), 'Категория')
        self.assertEqual(gettext('Описание'), 'Описание')
        self.assertEqual(gettext('Электроника'), 'Электроника')

    def test_english_localization(self):
        """Тест английской локализации."""
        activate('en')

        # Проверяем переводы на английский
        self.assertEqual(gettext('Категория'), 'Category')
        self.assertEqual(gettext('Описание'), 'Description')
        self.assertEqual(gettext('Электроника'), 'Electronics')
        self.assertEqual(gettext('Поиск'), 'Search')
        self.assertEqual(gettext('Новый'), 'New')
        self.assertEqual(gettext('Б/у'), 'Used')

    def test_status_translations(self):
        """Тест переводов статусов."""
        activate('en')

        self.assertEqual(gettext('Ожидает'), 'Pending')
        self.assertEqual(gettext('Принята'), 'Accepted')
        self.assertEqual(gettext('Отклонена'), 'Rejected')

    def test_error_messages_translations(self):
        """Тест переводов сообщений об ошибках."""
        activate('en')

        self.assertEqual(
            gettext('Заголовок должен содержать минимум 3 символа.'),
            'Title must contain at least 3 characters.'
        )
        self.assertEqual(
            gettext('Описание должно содержать минимум 10 символов.'),
            'Description must contain at least 10 characters.'
        )

    def test_form_field_translations(self):
        """Тест переводов полей форм."""
        activate('en')

        self.assertEqual(gettext('Имя пользователя'), 'Username')
        self.assertEqual(gettext('Пароль'), 'Password')
        self.assertEqual(gettext('Email'), 'Email')
