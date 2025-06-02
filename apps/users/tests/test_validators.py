from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import translation

from ..validators import PasswordValidator


class PasswordValidatorTest(TestCase):
    """Тесты кастомного валидатора пароля"""

    def setUp(self):
        self.validator = PasswordValidator()
        # Активируем английскую локализацию для тестов
        translation.activate('en')

    def test_valid_password(self):
        """Тест валидного пароля"""
        # Должен пройти без исключений
        try:
            self.validator.validate('Password123')
        except ValidationError:
            self.fail("Валидный пароль не должен вызывать ошибки")

    def test_password_no_digit(self):
        """Тест пароля без цифры"""
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate('PasswordABC')
        self.assertEqual(cm.exception.code, 'password_no_digit')

    def test_password_no_uppercase(self):
        """Тест пароля без заглавной буквы"""
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate('password123')
        self.assertEqual(cm.exception.code, 'password_no_upper')

    def test_password_no_digit_and_uppercase(self):
        """Тест пароля без цифры и заглавной буквы"""
        with self.assertRaises(ValidationError):
            self.validator.validate('password')

    def test_get_help_text(self):
        """Тест получения текста справки"""
        help_text = self.validator.get_help_text()
        # Проверяем английский текст
        self.assertIn('digit', help_text)
        self.assertIn('uppercase', help_text)
